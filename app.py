import streamlit as st
import requests
import urllib.parse
import json
import re
from datetime import datetime, timezone, time, timedelta
import zoneinfo
from pysolar.solar import get_azimuth, get_altitude
import streamlit.components.v1 as components

st.set_page_config(page_title="Girouette Malouine", layout="wide")

tz_france = zoneinfo.ZoneInfo("Europe/Paris")

if "onglet" not in st.session_state:
    st.session_state["onglet"] = "bronzette"

now_france = datetime.now(tz_france)
if "heure_selectionnee_str" not in st.session_state:
    m_init = 15 * round(now_france.minute / 15)
    h_init = now_france.hour
    if m_init == 60:
        h_init = (h_init + 1) % 24
        m_init = 0
    st.session_state["heure_selectionnee_str"] = f"{h_init:02d}:{m_init:02d}"

if "choix_jour" not in st.session_state:
    st.session_state["choix_jour"] = "Aujourd'hui"

def reinitialiser_heure():
    m_curr = 15 * round(datetime.now(tz_france).minute / 15)
    h_curr = datetime.now(tz_france).hour
    if m_curr == 60:
        h_curr = (h_curr + 1) % 24
        m_curr = 0
    st.session_state["heure_selectionnee_str"] = f"{h_curr:02d}:{m_curr:02d}"
    st.session_state["choix_jour"] = "Aujourd'hui"

def evaluer_confort(temp_air, vitesse_vent, rad, pluie, est_abrite):
    if pluie > 0.2:
        return "🌧️ PLUIE / PAS TOP", "#cc0000"

    vent_ressenti = 0 if est_abrite else vitesse_vent

    if vent_ressenti > 22 or vitesse_vent > 25:
        return "💨 TROP FRAIS", "#cc0000"

    if temp_air >= 20 and rad > 200 and vent_ressenti < 12:
        return "☀️ TOP CONDITION", "#2d5a27"
    elif rad > 50 and vent_ressenti < 15 and temp_air >= 20:
        return "😎 AGREABLE", "#38761d"
    elif temp_air >= 18 and temp_air < 20:
        return "⛅ UN PEU JUSTE", "#e69138"
    else:
        return "💨 TROP FRAIS", "#cc0000"

def evaluer_conditions_chasse(v_vent, h_vague, pluie):
    if pluie > 0.5:
        return "🔴 Eaux chargées (Pluies récentes)", "Le run des rivières / ruisseaux plombe la visibilité côtière.", "#cc0000"
    if h_vague > 1.2:
        return "🔴 Trop agité (Houle forte)", "Fond brassé, visibilité nulle et risque de clapot dangereux.", "#cc0000"
    if v_vent > 25:
        return "🟠 Vent fort (Clapot de surface)", "Navigabilité et surface compliquées, visibilité dégradée.", "#e69138"
    if h_vague < 0.5 and v_vent < 15:
        return "🟢 Top conditions (Mer d'huile)", "Excellentes dispositions pour de l'eau claire et un plan d'eau plat.", "#2d5a27"
    return "🟡 Correct / Modéré", "Visibilité correcte mais vigilance selon l'orientation du spot.", "#e69138"

@st.cache_data(ttl=3600)
def _fetch_horaire_maree_site():
    try:
        url = "https://horaire-maree.fr/maree/SAINT-MALO/"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        resp = requests.get(url, headers=headers, timeout=5)
        return resp.text
    except Exception:
        return ""

def calculer_temperature_mer_plage(dt_cible):
    jour_annee = dt_cible.timetuple().tm_yday
    points_cotiers = [
        (1, 9.8), (46, 9.5), (74, 10.2), (105, 11.8), (135, 13.8), (166, 16.5),
        (196, 18.8), (227, 19.9), (258, 19.7), (288, 17.2), (319, 14.2), (350, 11.8), (366, 10.0)
    ]
    for i in range(len(points_cotiers) - 1):
        j1, t1 = points_cotiers[i]
        j2, t2 = points_cotiers[i+1]
        if j1 <= jour_annee <= j2:
            fraction = (jour_annee - j1) / (j2 - j1)
            return round(t1 + fraction * (t2 - t1), 1)
    return 19.7

def récupérer_marées_réelles(dt_cible):
    try:
        html = _fetch_horaire_maree_site()
        heure_curr_str = dt_cible.strftime("%H:%M")
        delta_jours = (dt_cible.date() - now_france.date()).days
        
        raw_heures = re.findall(r'(\d{2}[h:]\d{2})', html)
        heures = [h.replace("h", ":") for h in raw_heures]
        
        uniques = []
        for h in heures:
            if h not in uniques:
                uniques.append(h)
                
        start_idx = delta_jours * 4
        
        if start_idx + 4 <= len(uniques):
            heures_jour = uniques[start_idx : start_idx + 4]
        else:
            heures_jour = ["01:52", "07:22", "14:10", "19:39"]

        bms = [heures_jour[0], heures_jour[2]]
        pms = [heures_jour[1], heures_jour[3]]

        next_pm = next((h for h in pms if h >= heure_curr_str), pms[0] if pms else "--:--")
        next_bm = next((h for h in bms if h >= heure_curr_str), bms[0] if bms else "--:--")
        
        return next_pm, next_bm
    except Exception:
        return "--:--", "--:--"

def récupérer_prochaines_marées_rance(dt_cible):
    data_rance = {
        "2026-09-14": {"hauts": ["00:00", "11:40"], "bas": ["07:30", "19:45"]},
        "2026-09-15": {"hauts": ["12:05", "23:50"], "bas": ["08:00", "20:10"]},
        "2026-09-16": {"hauts": ["00:25", "12:40"], "bas": ["08:20", "20:25"]},
        "2026-09-17": {"hauts": ["00:40", "13:00"], "bas": ["08:30", "20:45"]},
        "2026-09-18": {"hauts": ["01:15", "11:45"], "bas": ["08:45", "21:20"]},
        "2026-09-19": {"hauts": ["01:55", "14:05"], "bas": ["09:30", "22:10"]},
        "2026-09-20": {"hauts": ["02:10", "15:00"], "bas": ["10:10", "23:40"]}
    }
    date_str = dt_cible.strftime("%Y-%m-%d")
    info = data_rance.get(date_str, {"hauts": ["--:--"], "bas": ["--:--"]})
    
    heure_curr_str = dt_cible.strftime("%H:%M")
    
    prochain_haut = next((h for h in info["hauts"] if h >= heure_curr_str), info["hauts"][0] if info["hauts"] else "--:--")
    prochain_bas = next((b for b in info["bas"] if b >= heure_curr_str), info["bas"][0] if info["bas"] else "--:--")
    
    return prochain_haut, prochain_bas

# Styles dynamiques des 5 onglets
style_bronzette = "background-color: #436e64 !important; color: #f0ede6 !important;" if st.session_state["onglet"] == "bronzette" else "background-color: #f0ede6 !important; color: #436e64 !important;"
style_apero = "background-color: #436e64 !important; color: #f0ede6 !important;" if st.session_state["onglet"] == "apero" else "background-color: #f0ede6 !important; color: #436e64 !important;"
style_plongee = "background-color: #436e64 !important; color: #f0ede6 !important;" if st.session_state["onglet"] == "plongee" else "background-color: #f0ede6 !important; color: #436e64 !important;"
style_peche = "background-color: #436e64 !important; color: #f0ede6 !important;" if st.session_state["onglet"] == "peche" else "background-color: #f0ede6 !important; color: #436e64 !important;"
style_webcam = "background-color: #436e64 !important; color: #f0ede6 !important;" if st.session_state["onglet"] == "webcam" else "background-color: #f0ede6 !important; color: #436e64 !important;"

st.markdown(f"""
<style>
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    .stApp {{ background-color: #64978b !important; }}
    
    div[data-testid="stExpander"] button div p {{ color: #f0ede6 !important; font-weight: bold !important; }}
    div[data-testid="stExpander"] label p {{ color: #f0ede6 !important; font-weight: bold !important; }}
    
    .centrage-fixe {{ display: flex; flex-direction: row; justify-content: center; gap: 20px; flex-wrap: wrap; }}
    
    .rect-style {{ 
        background-color: rgba(240, 237, 230, 0.85) !important; 
        border-radius: 15px; 
        box-shadow: 0 8px 16px rgba(0,0,0,0.15); 
        overflow: hidden; 
        backdrop-filter: blur(5px);
    }}
    
    .plage-card {{ 
        padding: 0px 0px 15px 0px; 
        text-align: center !important; 
        width: 260px; 
        display: flex !important; 
        flex-direction: column !important; 
        align-items: center !important; 
        justify-content: flex-start !important; 
    }}
    
    .card-img {{ width: 100%; height: 140px; object-fit: cover; display: block; }}
    
    .card-title-clickable {{ 
        width: 100% !important; 
        margin: 10px 0 4px 0 !important; 
        padding: 0 !important;
        font-size: 1.15em !important; 
        font-weight: bold !important;
        text-decoration: underline !important; 
        color: #436e64 !important;
        text-align: center !important;
        cursor: pointer !important;
        display: block !important;
    }}
    
    .card-text {{ width: 100%; color: #444; margin: 0 0 10px 0; font-size: 0.85em; text-align: center !important; }}

    .title-wrapper {{
        display: flex;
        justify-content: center;
        width: 100%;
    }}

    .title-box-full {{
        background-color: #f0ede6;
        border-radius: 12px;
        padding: 14px 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        width: 100%;
        max-width: 600px;
        margin-bottom: 15px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }}
    .title-box-full h1 {{
        margin: 0 !important;
        padding: 0 !important;
        color: #436e64 !important;
        font-size: 1.4em !important;
        text-align: center !important;
    }}
    .title-box-full p {{
        margin: 6px 0 0 0 !important;
        padding: 0 !important;
        color: #557a70 !important;
        font-size: 0.9em !important;
        text-align: center !important;
    }}

    .title-box-section {{
        background-color: #f0ede6;
        border-radius: 12px;
        padding: 10px 20px;
        text-align: center !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        max-width: 350px;
        margin: 0 auto;
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    .title-box-section h3 {{
        margin: 0 !important;
        padding: 0 !important;
        color: #436e64 !important;
        font-size: 1.2em !important;
        text-align: center !important;
        width: 100% !important;
    }}
    
    /* Boutons de navigation (5 colonnes) */
    div[data-testid="stColumn"]:nth-child(2) button {{ {style_bronzette} border: 2px solid #436e64 !important; font-weight: bold !important; border-radius: 10px !important; padding: 6px 8px !important; font-size: 0.9em !important; }}
    div[data-testid="stColumn"]:nth-child(2) button p {{ color: inherit !important; font-weight: bold !important; }}

    div[data-testid="stColumn"]:nth-child(3) button {{ {style_apero} border: 2px solid #436e64 !important; font-weight: bold !important; border-radius: 10px !important; padding: 6px 8px !important; font-size: 0.9em !important; }}
    div[data-testid="stColumn"]:nth-child(3) button p {{ color: inherit !important; font-weight: bold !important; }}

    div[data-testid="stColumn"]:nth-child(4) button {{ {style_plongee} border: 2px solid #436e64 !important; font-weight: bold !important; border-radius: 10px !important; padding: 6px 8px !important; font-size: 0.9em !important; }}
    div[data-testid="stColumn"]:nth-child(4) button p {{ color: inherit !important; font-weight: bold !important; }}

    div[data-testid="stColumn"]:nth-child(5) button {{ {style_peche} border: 2px solid #436e64 !important; font-weight: bold !important; border-radius: 10px !important; padding: 6px 8px !important; font-size: 0.9em !important; }}
    div[data-testid="stColumn"]:nth-child(5) button p {{ color: inherit !important; font-weight: bold !important; }}

    div[data-testid="stColumn"]:nth-child(6) button {{ {style_webcam} border: 2px solid #436e64 !important; font-weight: bold !important; border-radius: 10px !important; padding: 6px 8px !important; font-size: 0.9em !important; }}
    div[data-testid="stColumn"]:nth-child(6) button p {{ color: inherit !important; font-weight: bold !important; }}

    div[data-testid="stExpander"] button[kind="secondary"] {{
        background-color: #f0ede6 !important;
        border: 1px solid #436e64 !important;
        margin-top: 28px !important;
    }}
    div[data-testid="stExpander"] button[kind="secondary"] p {{
        color: #436e64 !important;
        font-weight: bold !important;
        -webkit-text-fill-color: #436e64 !important;
    }}

    div[data-testid="stSelectbox"] > div > div {{
        background-color: #f0ede6 !important;
        border: 1px solid #436e64 !important;
        color: #436e64 !important;
        border-radius: 8px !important;
    }}
    div[data-testid="stSelectbox"] div[role="combobox"] {{
        color: #436e64 !important;
        font-weight: bold !important;
        text-align: center !important;
        justify-content: center !important;
        -webkit-text-fill-color: #436e64 !important;
    }}
</style>
""", unsafe_allow_html=True)

LAT_SM, LON_SM = 48.6493, -2.0089

dirs_code_16 = [
    "N", "NNE", "NE", "ENE",
    "E", "ESE", "SE", "SSE",
    "S", "SSW", "SW", "WSW",
    "W", "WNW", "NW", "NNW", "N"
]

adjacents = {
    "N": ["N", "NNE", "NNW"],
    "NNE": ["NNE", "N", "NE"],
    "NE": ["NE", "NNE", "ENE", "N", "E"],
    "ENE": ["ENE", "NE", "E"],
    "E": ["E", "ENE", "ESE"],
    "SE": ["SE", "ESE", "SSE", "E", "S"],
    "SSE": ["SSE", "SE", "S"],
    "S": ["S", "SSE", "SSW"],
    "SSW": ["SSW", "S", "SW"],
    "SW": ["SW", "SSW", "WSW", "S", "W"],
    "WSW": ["WSW", "SW", "W"],
    "W": ["W", "WSW", "WNW"],
    "WNW": ["WNW", "W", "NW"],
    "NW": ["NW", "WNW", "NNW", "W", "N"],
    "NNW": ["NNW", "NW", "N"]
}

st.markdown("""
<div class='title-wrapper'>
    <div class='title-box-full'>
        <h1>Girouette Malouine</h1>
        <p>Météo, bronzette, apéros & plongée à l'abri du vent</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Barre de navigation à 5 onglets
_, nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, _ = st.columns([0.2, 1.6, 1.6, 1.6, 1.6, 1.6, 0.2])

with nav_col1:
    if st.button("🏖️ Bronzette", use_container_width=True):
        st.session_state["onglet"] = "bronzette"
        st.rerun()

with nav_col2:
    if st.button("🍹 Apéro", use_container_width=True):
        st.session_state["onglet"] = "apero"
        st.rerun()

with nav_col3:
    if st.button("🤿 Plongée", use_container_width=True):
        st.session_state["onglet"] = "plongee"
        st.rerun()

with nav_col4:
    if st.button("🎣 Pêche", use_container_width=True):
        st.session_state["onglet"] = "peche"
        st.rerun()

with nav_col5:
    if st.button("📹 Webcam", use_container_width=True):
        st.session_state["onglet"] = "webcam"
        st.rerun()

st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

liste_heures = [f"{h:02d}:{m:02d}" for h in range(24) for m in (0, 15, 30, 45)]

if st.session_state["heure_selectionnee_str"] not in liste_heures:
    h_curr, m_curr = map(int, st.session_state["heure_selectionnee_str"].split(":"))
    m_round = 15 * round(m_curr / 15)
    if m_round == 60:
        h_curr = (h_curr + 1) % 24
        m_round = 0
    st.session_state["heure_selectionnee_str"] = f"{h_curr:02d}:{m_round:02d}"

with st.expander("⚙️ Options & Horaire de simulation"):
    col_date, col_time = st.columns([1, 1])
    with col_date:
        choix_jour = st.radio("Jour de simulation", ["Aujourd'hui", "Demain"], key="choix_jour", horizontal=True)
    with col_time:
        heure_str = st.selectbox("Choisir une heure", options=liste_heures, key="heure_selectionnee_str")
        
    st.button("🔄 Réinitialiser à l'heure actuelle", on_click=reinitialiser_heure, use_container_width=True)
    use_manual = st.checkbox("Activer le mode météo manuelle")

heure_h, heure_m = map(int, heure_str.split(":"))
heure_selectionnee = time(heure_h, heure_m)

date_cible = now_france.date()
if choix_jour == "Demain":
    date_cible += timedelta(days=1)

dt_local = datetime.combine(date_cible, heure_selectionnee).replace(tzinfo=tz_france)
dt_utc = dt_local.astimezone(timezone.utc)

label_jour = f"pour {heure_selectionnee.strftime('%H:%M')}" if choix_jour == "Aujourd'hui" else f"pour Demain à {heure_selectionnee.strftime('%H:%M')}"

sol_alt = get_altitude(LAT_SM, LON_SM, dt_utc)
sol_azi = get_azimuth(LAT_SM, LON_SM, dt_utc)

est_passe = (choix_jour == "Aujourd'hui" and dt_local < now_france - timedelta(minutes=35))
est_instant_present = (choix_jour == "Aujourd'hui" and abs((dt_local - now_france).total_seconds()) < 1800)

try:
    url_météo = (
        f"https://api.open-meteo.com/v1/forecast?latitude={LAT_SM}&longitude={LON_SM}"
        "&current=temperature_2m,wind_speed_10m,wind_direction_10m"
        "&hourly=temperature_2m,wind_speed_10m,wind_direction_10m,direct_radiation,precipitation"
    )
    r = requests.get(url_météo, timeout=5).json()
    
    if est_passe:
        temp_air = None
        auto_v = 0
        auto_a = 0.0
        rad = 0.0
        pluie = 0.0
        soleil_txt = "⏳ Heure passée"
    elif est_instant_present and "current" in r:
        temp_air = round(r["current"]["temperature_2m"], 1)
        auto_v = int(r["current"]["wind_speed_10m"])
        auto_a = float(r["current"]["wind_direction_10m"])
        rad = 300.0  
        pluie = 0.0
        soleil_txt = "☀️ Ensoleillé / Direct"
    else:
        iso_cible = dt_local.strftime("%Y-%m-%dT%H:00")
        if "hourly" in r and iso_cible in r["hourly"]["time"]:
            idx = r["hourly"]["time"].index(iso_cible)
        else:
            idx = 0
        
        auto_v = int(r["hourly"]["wind_speed_10m"][idx])
        auto_a = float(r["hourly"]["wind_direction_10m"][idx])
        temp_air = round(r["hourly"]["temperature_2m"][idx], 1)
        rad = r["hourly"]["direct_radiation"][idx]
        pluie = r["hourly"]["precipitation"][idx]
        
        if pluie > 0.2:
            soleil_txt = "🌧️ Pluie"
        elif rad > 400:
            soleil_txt = "☀️ Plein soleil"
        elif rad > 150:
            soleil_txt = "⛅ Éclaircies"
        elif rad > 20:
            soleil_txt = "☁️ Nuageux"
        else:
            soleil_txt = "☁️ Couvert"
except:
    auto_v, auto_a = 15, 270.0
    temp_air = 18.0
    rad = 300.0
    pluie = 0.0
    soleil_txt = "☀️ Ensoleillé"

try:
    rm = requests.get(f"https://marine-api.open-meteo.com/v1/marine?latitude={LAT_SM}&longitude={LON_SM}&current=wave_height,wave_period", timeout=5).json()
    wave_height = rm.get("current", {}).get("wave_height", 0.5)
    wave_period = rm.get("current", {}).get("wave_period", 6.0)
except:
    wave_height = 0.5
    wave_period = 6.0

temp_mer = calculer_temperature_mer_plage(dt_local)

haute_mer, basse_mer = récupérer_marées_réelles(dt_local)
rance_haut, rance_bas = récupérer_prochaines_marées_rance(dt_local)

if use_manual:
    with st.expander("⚙️ Options & Horaire de simulation", expanded=True):
        vitesse = st.slider("Vitesse vent (km/h)", 0, 80, auto_v)
        angle = float(st.slider("Direction vent ( deg )", 0, 360, int(auto_a)))
else:
    vitesse, angle = auto_v, auto_a

idx_dir = int(round((angle % 360) / 22.5))
ori_code = dirs_code_16[idx_dir]

# -----------------------------------------------------------------------------
# ONGLET 1 : BRONZETTE
# -----------------------------------------------------------------------------
if st.session_state["onglet"] == "bronzette":
    if est_passe:
        st.markdown(f"<div class='rect-style' style='padding:12px; text-align:center; max-width:680px; margin:15px auto 25px auto; color:#222;'><b>Bronzette {label_jour}</b><br><i>Données non disponibles pour les heures passées.</i></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='rect-style' style='padding:12px; text-align:center; max-width:680px; margin:15px auto 25px auto; color:#222;'>
            <b>Bronzette {label_jour}</b><br>
            Vent : {vitesse} km/h ({ori_code}) | Air : <b>{temp_air}°C</b> | Mer : <b>~{temp_mer}°C</b> | <b>{soleil_txt}</b><br>
            🌊 <b>Mer :</b> PM {haute_mer} — BM {basse_mer}<br>
            🔒 <b>Rance :</b> Haut {rance_haut} — Bas {rance_bas}
        </div>
        """, unsafe_allow_html=True)

    if est_passe:
        st.markdown("<div class='rect-style' style='padding:20px; text-align:center; color:#222;'><b>Veuillez sélectionner une heure future ou l'heure actuelle pour simuler les conditions.</b></div>", unsafe_allow_html=True)
    elif sol_alt <= 2:
        st.markdown("<div class='rect-style' style='padding:20px; text-align:center; color:#222;'><b>🌙 Le soleil est couché à cette heure-là ! Pas de bronzette possible.</b></div>", unsafe_allow_html=True)
    else:
        plages = [
            {"Nom": "La Passagere", "Ville": "Saint-Malo", "Min": 315, "Max": 135, "Image": "Passagere.jpg"},
            {"Nom": "Fours a Chaux", "Ville": "Saint-Malo", "Min": 315, "Max": 135, "Image": "Foursachaux.jpg"},
            {"Nom": "Saint-Pere", "Ville": "Saint-Malo", "Min": 315, "Max": 135, "Image": "Saint-Pere.jpg"},
            {"Nom": "Les Sablons", "Ville": "Saint-Malo", "Min": 45, "Max": 225, "Image": "Sablons.jpg"},
            {"Nom": "Bon-Secours", "Ville": "Saint-Malo", "Min": 360, "Max": 180, "Image": "Bonsecours.jpg"},
            {"Nom": "L'Eventail", "Ville": "Saint-Malo", "Min": 360, "Max": 180, "Image": "Eventail.jpg"},
            {"Nom": "Le Sillon", "Ville": "Saint-Malo", "Min": 45, "Max": 225, "Image": "Sillon.jpg"},
            {"Nom": "Le Môle", "Ville": "Saint-Malo", "Min": 0, "Max": 180, "Image": "Mole.jpg"},
            {"Nom": "Le Val", "Ville": "Rotheneuf", "Min": 45, "Max": 225, "Image": "Val.jpg"},
            {"Nom": "Les Chevrets", "Ville": "Saint-Coulomb", "Min": 22, "Max": 202, "Image": "Chevrets.jpg"},
            {"Nom": "La Touesse", "Ville": "Saint-Coulomb", "Min": 90, "Max": 270, "Image": "Touesse.jpg"},
            {"Nom": "Le Guesclin", "Ville": "Saint-Coulomb", "Min": 45, "Max": 225, "Image": "Guesclin.jpg"},
            {"Nom": "Le Verger", "Ville": "Saint-Coulomb", "Min": 45, "Max": 225, "Image": "Verger.jpg"},
            {"Nom": "Port Mer", "Ville": "Cancale", "Min": 180, "Max": 360, "Image": "Portmer.jpg"}
        ]

        abritees = [p for p in plages if (True if vitesse < 12 else (p["Min"] <= angle <= p["Max"] if p["Min"] <= p["Max"] else (angle >= p["Min"] or angle <= p["Max"])))]
        exposees = [p for p in plages if p not in abritees]

        st.markdown("<div class='title-box-section' style='margin-bottom: 20px;'><h3>A l'abri</h3></div>", unsafe_allow_html=True)
        html_a = "<div class='centrage-fixe'>"
        for p in abritees:
            badge_txt, badge_color = evaluer_confort(temp_air, vitesse, rad, pluie, est_abrite=True)
            q = urllib.parse.quote(p['Nom'] + " " + p['Ville'])
            target_url = f"https://google.com/search?q={q}"
            img_url = f"https://raw.githubusercontent.com/Ludo110/girouette/main/{p['Image']}"
            palmier_url = f"https://raw.githubusercontent.com/Ludo110/girouette/main/Palmier.png"
            html_a += f"<div class='plage-card rect-style'><img src='{img_url}' class='card-img' onerror=\"this.src='{palmier_url}';\"><div class='card-title-clickable' onclick=\"window.open('{target_url}', '_blank');\">{p['Nom']}</div><p class='card-text'>{p['Ville']}</p><b style='color:{badge_color};'>{badge_txt}</b></div>"
        html_a += "</div>"
        st.markdown(html_a, unsafe_allow_html=True)

        st.markdown("<div class='title-box-section' style='margin-top: 30px; margin-bottom: 20px;'><h3>Exposées</h3></div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        milieu = len(exposees) // 2

        def afficher_colonne(liste_plages, colonne):
            with colonne:
                for p in liste_plages:
                    q = urllib.parse.quote(p['Nom'] + " " + p['Ville'])
                    st.markdown(f"<div style='text-align:center; margin-bottom:10px;'><a href='https://google.com/search?q={q}' style='color:white;' target='_blank'>{p['Nom']} ({p['Ville']})</a></div>", unsafe_allow_html=True)

        afficher_colonne(exposees[:milieu], col1)
        afficher_colonne(exposees[milieu:], col2)

# -----------------------------------------------------------------------------
# ONGLET 2 : APÉRO AU SOLEIL
# -----------------------------------------------------------------------------
elif st.session_state["onglet"] == "apero":
    if est_passe:
        st.markdown(f"<div class='rect-style' style='padding:12px; text-align:center; max-width:680px; margin:15px auto 25px auto; color:#222;'><b>Apéro {label_jour}</b><br><i>Données non disponibles pour les heures passées.</i></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='rect-style' style='padding:12px; text-align:center; max-width:680px; margin:15px auto 25px auto; color:#222;'>
            <b>Apéro {label_jour}</b><br>
            Vent : {vitesse} km/h ({ori_code}) | Air : <b>{temp_air}°C</b> | Mer : <b>~{temp_mer}°C</b> | <b>{soleil_txt}</b><br>
            🌊 <b>Mer :</b> PM {haute_mer} — BM {basse_mer}<br>
            🔒 <b>Rance :</b> Haut {rance_haut} — Bas {rance_bas}
        </div>
        """, unsafe_allow_html=True)

    try:
        with open("spots_apero.json", "r", encoding="utf-8") as f:
            spots = json.load(f)
    except Exception as e:
        spots = []

    if est_passe:
        pass
    elif sol_alt <= 2:
        st.markdown("<div class='rect-style' style='padding:20px; text-align:center; color:#222;'><b>🌙 Le soleil sera couché à cette heure-là !</b></div>", unsafe_allow_html=True)
    else:
        spots_valides = []
        v_compatibles = adjacents.get(ori_code, [ori_code])

        for s in spots:
            au_soleil = (s["soleil_azimut_min"] <= sol_azi <= s["soleil_azimut_max"])
            abrite_vent = True if vitesse < 15 else any(vc in s["vents_abrites"] for vc in v_compatibles)
            
            if au_soleil and abrite_vent:
                spots_valides.append(s)

        st.markdown("<div class='title-box-section' style='margin-bottom: 20px;'><h3>Top Spots Apéro</h3></div>", unsafe_allow_html=True)

        if spots_valides:
            html_apero = "<div class='centrage-fixe'>"
            for s in spots_valides:
                badge_txt, badge_color = evaluer_confort(temp_air, vitesse, rad, pluie, est_abrite=True)
                q = urllib.parse.quote(s['nom'] + " Saint-Malo")
                target_url = f"https://google.com/search?q={q}"
                html_apero += f"<div class='plage-card rect-style' style='padding:15px;'><div class='card-title-clickable' onclick=\"window.open('{target_url}', '_blank');\">{s['nom']}</div><p class='card-text'><b>{s['type']}</b><br>{s['description']}</p><b style='color:{badge_color};'>{badge_txt} 🍹</b></div>"
            html_apero += "</div>"
            st.markdown(html_apero, unsafe_allow_html=True)
        else:
            st.markdown("<div class='rect-style' style='padding:20px; text-align:center; color:#222;'>Aucun spot idéal trouvé à cette heure-là pour cette orientation de vent/soleil.</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# ONGLET 3 : PLONGÉE & CHASSE SOUS-MARINE
# -----------------------------------------------------------------------------
elif st.session_state["onglet"] == "plongee":
    if est_passe:
        st.markdown(f"<div class='rect-style' style='padding:12px; text-align:center; max-width:680px; margin:15px auto 25px auto; color:#222;'><b>Plongée & Chasse {label_jour}</b><br><i>Données non disponibles pour les heures passées.</i></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='rect-style' style='padding:12px; text-align:center; max-width:680px; margin:15px auto 25px auto; color:#222;'>
            <b>Plongée & Chasse {label_jour}</b><br>
            Vent : {vitesse} km/h ({ori_code}) | Air : <b>{temp_air}°C</b> | Mer : <b>~{temp_mer}°C</b><br>
            🌊 <b>Mer :</b> PM {haute_mer} — BM {basse_mer}<br>
            🔒 <b>Rance :</b> Haut {rance_haut} — Bas {rance_bas}
        </div>
        """, unsafe_allow_html=True)

        statut, conseil, couleur = evaluer_conditions_chasse(vitesse, wave_height, pluie)

        st.markdown(f"""
        <div class='rect-style' style='padding:25px; max-width:600px; margin:0 auto; color:#222;'>
            <h3 style='text-align:center; color:#436e64; margin-top:0;'>Conditions Sous-Marines Estimées</h3>
            <div style='text-align:center; font-size:1.2em; font-weight:bold; color:{couleur}; margin-bottom:10px;'>{statut}</div>
            <p style='text-align:center; font-style:italic; margin-bottom:20px;'>{conseil}</p>
            <hr style='border:0; border-top:1px solid #ccc; margin:15px 0;'>
            <div style='display:flex; justify-content:space-around; flex-wrap:wrap; gap:15px; text-align:center;'>
                <div><b>Hauteur de vagues</b><br>{wave_height} m</div>
                <div><b>Période de houle</b><br>{wave_period} s</div>
                <div><b>Température de l'eau</b><br>~{temp_mer}°C</div>
                <div><b>Pluie récente</b><br>{pluie} mm</div>
            </div>
            <div style='margin-top:20px; font-size:0.9em; text-align:center; color:#555;'>
                💡 <i>Rappel : Pour la chasse sur Saint-Malo, ciblez idéalement une fenêtre de 2 heures autour de la basse ({basse_mer}) pour profiter de l'étale et d'une eau plus claire.</i>
            </div>
            <div style='margin-top:15px; padding:12px; background-color: rgba(204,0,0,0.1); border-left: 4px solid #cc0000; border-radius: 4px; font-size:0.85em; text-align:left; color:#444;'>
                ⚠️ <b>Avertissement de sécurité :</b> Ces données sont fournies à titre indicatif et ne se substituent en aucun cas à votre propre jugement sur place. En mer, les conditions peuvent changer rapidement. Ne prenez jamais de risques inutiles.
            </div>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# ONGLET 4 : PÊCHE & ACTIVITÉ SOLUNAIRE
# -----------------------------------------------------------------------------
elif st.session_state["onglet"] == "peche":
    st.markdown(f"""
    <div class='rect-style' style='padding:12px; text-align:center; max-width:680px; margin:15px auto 25px auto; color:#222;'>
        <b>Activité Pêche & Solunaire {label_jour}</b><br>
        🌊 <b>Mer :</b> PM {haute_mer} — BM {basse_mer}<br>
        🔒 <b>Rance :</b> Haut {rance_haut} — Bas {rance_bas}
    </div>
    """, unsafe_allow_html=True)

    components.html("""
    <div class="rect-style" style="background-color: rgba(240, 237, 230, 0.85); border-radius: 15px; padding: 25px; max-width: 650px; margin: 0 auto; color: #222; text-align: center; font-family: sans-serif; box-shadow: 0 8px 16px rgba(0,0,0,0.15);">
        <h3 style="color:#436e64; margin-top:0;">Activité modérée</h3>
        <p style="margin: 5px 0 15px 0; font-size: 0.95em; color:#555;">🟣 Premier croissant · Coef. 74</p>
        
        <div style="background: rgba(255,255,255,0.7); border-radius: 12px; padding: 10px; margin-bottom: 20px; font-weight: bold; color:#333;">
            Prochaine période dans 3 h 26
        </div>

        <div style="display: flex; flex-direction: column; gap: 8px;">
            <div style="background: rgba(255,255,255,0.5); padding: 12px 15px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
                <b style="color:#436e64;">Période majeure</b>
                <span>04h47 → 06h47 <i style="font-size:0.85em; color:#555;">Montante</i></span>
            </div>
            <div style="background: rgba(255,255,255,0.5); padding: 12px 15px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
                <b style="color:#557a70;">Période mineure</b>
                <span>13h39 → 14h39 <i style="font-size:0.85em; color:#555;">Descendante</i></span>
            </div>
            <div style="background: rgba(255,255,255,0.5); padding: 12px 15px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
                <b style="color:#436e64;">Période majeure</b>
                <span>17h08 → 19h08 <i style="font-size:0.85em; color:#555;">Montante</i></span>
            </div>
            <div style="background: rgba(255,255,255,0.5); padding: 12px 15px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
                <b style="color:#557a70;">Période mineure</b>
                <span>21h36 → 22h36 <i style="font-size:0.85em; color:#555;">Montante</i></span>
            </div>
        </div>

        <p style="margin-top:20px; font-size:0.8em; font-style:italic; color:#666;">
            Périodes solunaires indicatives (activité théorique des poissons). Marée et coefficient restent calculés.
        </p>
    </div>
    """, height=410, scrolling=False)

# -----------------------------------------------------------------------------
# ONGLET 5 : WEBCAM THERMES MARINS
# -----------------------------------------------------------------------------
elif st.session_state["onglet"] == "webcam":
    st.markdown(f"""
    <div class='rect-style' style='padding:12px; text-align:center; max-width:680px; margin:15px auto 25px auto; color:#222;'>
        <b>Webcam Thermes Marins en direct</b><br>
        🌊 <b>Mer :</b> PM {haute_mer} — BM {basse_mer}<br>
        🔒 <b>Rance :</b> Haut {rance_haut} — Bas {rance_bas}
    </div>
    """, unsafe_allow_html=True)

    components.html("""
    <div style="background-color: rgba(240, 237, 230, 0.9); border-radius: 15px; padding: 20px; max-width: 900px; margin: 0 auto; text-align: center; font-family: sans-serif; box-shadow: 0 8px 16px rgba(0,0,0,0.15);">
        <h3 style="color:#436e64; margin-top:0;">📹 Thermes Marins de Saint-Malo en direct</h3>
        
        <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); background: #000;">
            <iframe src="https://www.vision-environnement.com/live/player/stmalo40.php" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border:0;" scrolling="no" allowfullscreen="true" webkitallowfullscreen="true" mozallowfullscreen="true" allow="autoplay; fullscreen; picture-in-picture"></iframe>
        </div>

        <p style="margin-top:15px; font-size:0.9em; color:#444;">
            🌊 <i>Vue panoramique en direct depuis les Thermes Marins de Saint-Malo.</i>
        </p>
    </div>
    """, height=520, scrolling=False)
