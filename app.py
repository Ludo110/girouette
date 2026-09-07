import streamlit as st
import requests
import urllib.parse
import json
from datetime import datetime, timezone, time
import zoneinfo
from pysolar.solar import get_azimuth, get_altitude

st.set_page_config(page_title="Girouette Malouine", layout="wide")

# Gestion du fuseau horaire local (Saint-Malo / France)
tz_france = zoneinfo.ZoneInfo("Europe/Paris")

# Initialisation des états dans le session_state
if "onglet" not in st.session_state:
    st.session_state["onglet"] = "bronzette"

if "heure_simulee" not in st.session_state:
    st.session_state["heure_simulee"] = datetime.now(tz_france).time()

# Callback pour réinitialiser l'heure à l'heure locale actuelle
def reinitialiser_heure():
    st.session_state["heure_simulee"] = datetime.now(tz_france).time()

# Styles dynamiques pour les boutons d'onglets
style_bronzette = "background-color: #436e64 !important; color: #f0ede6 !important;" if st.session_state["onglet"] == "bronzette" else "background-color: #f0ede6 !important; color: #436e64 !important;"
style_apero = "background-color: #436e64 !important; color: #f0ede6 !important;" if st.session_state["onglet"] == "apero" else "background-color: #f0ede6 !important; color: #436e64 !important;"

st.markdown(f"""
<style>
    /* Masquer le header, le footer et le menu Streamlit */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    .stApp {{ background-color: #64978b !important; }}
    
    /* Titre expander et textes internes */
    div[data-testid="stExpander"] button div p {{ color: #f0ede6 !important; font-weight: bold !important; }}
    div[data-testid="stExpander"] label p {{ color: #f0ede6 !important; font-weight: bold !important; }}
    
    .centrage-fixe {{ display: flex; flex-direction: row; justify-content: center; gap: 20px; flex-wrap: wrap; }}
    
    /* Encadrés secondaires avec fond semi-transparent */
    .rect-style {{ 
        background-color: rgba(240, 237, 230, 0.85) !important; 
        border-radius: 15px; 
        box-shadow: 0 8px 16px rgba(0,0,0,0.15); 
        overflow: hidden; 
        backdrop-filter: blur(5px);
    }}
    
    /* Conteneur Flexbox strict pour la carte */
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
    
    /* Titre cliquable purement centré sans balises A encombrantes */
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

    /* Conteneur global centré */
    .title-wrapper {{
        display: flex;
        justify-content: center;
        width: 100%;
    }}

    /* Encadré principal */
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

    /* Encadrés des sections */
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
    
    /* Styling ciblé uniquement pour les boutons d'onglets haut de page */
    div[data-testid="stColumn"]:nth-child(2) button {{
        {style_bronzette}
        border: 2px solid #436e64 !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        padding: 6px 12px !important;
    }}
    div[data-testid="stColumn"]:nth-child(2) button p {{
        color: inherit !important;
        font-weight: bold !important;
    }}

    div[data-testid="stColumn"]:nth-child(3) button {{
        {style_apero}
        border: 2px solid #436e64 !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        padding: 6px 12px !important;
    }}
    div[data-testid="stColumn"]:nth-child(3) button p {{
        color: inherit !important;
        font-weight: bold !important;
    }}

    /* Style du bouton de réinitialisation dans l'expander */
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

    /* Force le style sur l'encadré et l'input de st.time_input */
    div[data-baseweb="input"], div[data-baseweb="input"] > div, div[data-baseweb="input"] input {{
        background-color: #f0ede6 !important;
        border-color: #436e64 !important;
        color: #436e64 !important;
        text-align: center !important;
        font-weight: bold !important;
        -webkit-text-fill-color: #436e64 !important;
        border-radius: 8px !important;
    }}
</style>
""", unsafe_allow_html=True)

LAT_SM, LON_SM = 48.6493, -2.0089
dirs = ["Nord", "Nord-Est", "Est", "Sud-Est", "Sud", "Sud-Ouest", "Ouest", "Nord-Ouest", "Nord"]

# 1. En-tête principal
st.markdown("""
<div class='title-wrapper'>
    <div class='title-box-full'>
        <h1>Girouette Malouine</h1>
        <p>Météo, bronzette & apéros à l'abri du vent</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 2. Boutons de navigation
_, nav_col1, nav_col2, _ = st.columns([1, 2, 2, 1])

with nav_col1:
    if st.button("🏖️ Bronzette", use_container_width=True):
        st.session_state["onglet"] = "bronzette"
        st.rerun()

with nav_col2:
    if st.button("🍹 Apéro au Soleil", use_container_width=True):
        st.session_state["onglet"] = "apero"
        st.rerun()

st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

# Expander de configuration horaire & météo
with st.expander("⚙️ Options & Horaire de simulation"):
    col_time, col_reset = st.columns([1, 1])
    with col_time:
        heure_selectionnee = st.time_input(
            "Choisir une heure pour la simulation", 
            key="heure_simulee"
        )
    with col_reset:
        st.button("🔄 Réinitialiser à l'heure actuelle", on_click=reinitialiser_heure, use_container_width=True)
    
    use_manual = st.checkbox("Activer le mode météo manuelle")

# Date/heure locale complète pour la simulation
now_france = datetime.now(tz_france)
dt_local = datetime.combine(now_france.date(), heure_selectionnee).replace(tzinfo=tz_france)
dt_utc = dt_local.astimezone(timezone.utc)

# Requête météo horaire Open-Meteo
try:
    r = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={LAT_SM}&longitude={LON_SM}&hourly=temperature_2m,wind_speed_10m,wind_direction_10m,direct_radiation", timeout=5).json()
    
    # Trouver l'index de l'heure correspondante
    heures = [datetime.fromisoformat(t).hour for t in r["hourly"]["time"]]
    idx = heures.index(heure_selectionnee.hour) if heure_selectionnee.hour in heures else 0
    
    auto_v = int(r["hourly"]["wind_speed_10m"][idx])
    auto_a = float(r["hourly"]["wind_direction_10m"][idx])
    temp_air = round(r["hourly"]["temperature_2m"][idx], 1)
    rad = r["hourly"]["direct_radiation"][idx]
    
    if rad > 400:
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
    soleil_txt = "☀️ Ensoleillé"

# Données mer
try:
    rm = requests.get(f"https://marine-api.open-meteo.com/v1/marine?latitude={LAT_SM}&longitude={LON_SM}&current=sea_surface_temperature", timeout=5).json()
    temp_mer = round(rm["current"]["sea_surface_temperature"], 1)
except:
    temp_mer = 16.0

if use_manual:
    with st.expander("⚙️ Options & Horaire de simulation", expanded=True):
        vitesse = st.slider("Vitesse vent (km/h)", 0, 80, auto_v)
        angle = float(st.slider("Direction vent ( deg )", 0, 360, int(auto_a)))
else:
    vitesse, angle = auto_v, auto_a

ori = dirs[int(round((angle % 360) / 45))]

# -----------------------------------------------------------------------------
# ONGLET 1 : BRONZETTE
# -----------------------------------------------------------------------------
if st.session_state["onglet"] == "bronzette":
    plages = [
        {"Nom": "La Passagere", "Ville": "Saint-Malo", "Min": 315, "Max": 135, "Image": "Passagere.jpg"},
        {"Nom": "Fours a Chaux", "Ville": "Saint-Malo", "Min": 315, "Max": 135, "Image": "Foursachaux.jpg"},
        {"Nom": "Saint-Pere", "Ville": "Saint-Malo", "Min": 315, "Max": 135, "Image": "Saint-Pere.jpg"},
        {"Nom": "Les Sablons", "Ville": "Saint-Malo", "Min": 45, "Max": 225, "Image": "Sablons.jpg"},
        {"Nom": "Bon-Secours", "Ville": "Saint-Malo", "Min": 360, "Max": 180, "Image": "Bonsecours.jpg"},
        {"Nom": "L'Eventail", "Ville": "Saint-Malo", "Min": 360, "Max": 180, "Image": "Eventail.jpg"},
        {"Nom": "Le Sillon", "Ville": "Saint-Malo", "Min": 45, "Max": 225, "Image": "Sillon.jpg"},
        {"Nom": "Le Val", "Ville": "Rotheneuf", "Min": 45, "Max": 225, "Image": "Val.jpg"},
        {"Nom": "Les Chevrets", "Ville": "Saint-Coulomb", "Min": 22, "Max": 202, "Image": "Chevrets.jpg"},
        {"Nom": "La Touesse", "Ville": "Saint-Coulomb", "Min": 90, "Max": 270, "Image": "Touesse.jpg"},
        {"Nom": "Le Guesclin", "Ville": "Saint-Coulomb", "Min": 45, "Max": 225, "Image": "Guesclin.jpg"},
        {"Nom": "Le Verger", "Ville": "Saint-Coulomb", "Min": 45, "Max": 225, "Image": "Verger.jpg"},
        {"Nom": "Port Mer", "Ville": "Cancale", "Min": 180, "Max": 360, "Image": "Portmer.jpg"}
    ]

    st.markdown(f"<div class='rect-style' style='padding:12px; text-align:center; max-width:540px; margin:15px auto 25px auto; color:#222;'><b>Prévisions pour {heure_selectionnee.strftime('%H:%M')}</b><br>Vent : {vitesse} km/h - {ori} ({int(angle)}°)<br>Air : <b>{temp_air}°C</b> | Mer : <b>{temp_mer}°C</b> | <b>{soleil_txt}</b></div>", unsafe_allow_html=True)

    abritees = [p for p in plages if (True if vitesse < 10 else (p["Min"] <= angle <= p["Max"] if p["Min"] <= p["Max"] else (angle >= p["Min"] or angle <= p["Max"])))]
    exposees = [p for p in plages if p not in abritees]

    st.markdown("<div class='title-box-section' style='margin-bottom: 20px;'><h3>A l'abri</h3></div>", unsafe_allow_html=True)
    html_a = "<div class='centrage-fixe'>"
    for p in abritees:
        q = urllib.parse.quote(p['Nom'] + " " + p['Ville'])
        target_url = f"https://google.com/search?q={q}"
        img_url = f"https://raw.githubusercontent.com/Ludo110/girouette/main/{p['Image']}"
        palmier_url = f"https://raw.githubusercontent.com/Ludo110/girouette/main/Palmier.png"
        html_a += f"<div class='plage-card rect-style'><img src='{img_url}' class='card-img' onerror=\"this.src='{palmier_url}';\"><div class='card-title-clickable' onclick=\"window.open('{target_url}', '_blank');\">{p['Nom']}</div><p class='card-text'>{p['Ville']}</p><b style='color:#2d5a27;'>IDEALE</b></div>"
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
    sol_alt = get_altitude(LAT_SM, LON_SM, dt_utc)
    sol_azi = get_azimuth(LAT_SM, LON_SM, dt_utc)

    st.markdown(f"<div class='rect-style' style='padding:12px; text-align:center; max-width:540px; margin:15px auto 25px auto; color:#222;'><b>Prévisions Apéro pour {heure_selectionnee.strftime('%H:%M')}</b><br>Vent : {vitesse} km/h ({ori}) — Soleil : Alt {int(sol_alt)}° / Azi {int(sol_azi)}°<br>Air : <b>{temp_air}°C</b> | Mer : <b>{temp_mer}°C</b> | <b>{soleil_txt}</b></div>", unsafe_allow_html=True)

    try:
        with open("spots_apero.json", "r", encoding="utf-8") as f:
            spots = json.load(f)
    except Exception as e:
        st.error("Impossible de charger spots_apero.json")
        spots = []

    spots_valides = []
    if sol_alt <= 2:
        st.markdown("<div class='rect-style' style='padding:20px; text-align:center; color:#222;'><b>🌙 Le soleil sera couché à cette heure-là !</b></div>", unsafe_allow_html=True)
    else:
        for s in spots:
            au_soleil = (s["soleil_azimut_min"] <= sol_azi <= s["soleil_azimut_max"])
            abrite_vent = True if vitesse < 10 else (ori in s["vents_abrites"])
            
            if au_soleil and abrite_vent:
                spots_valides.append(s)

        st.markdown("<div class='title-box-section' style='margin-bottom: 20px;'><h3>Top Spots Apéro</h3></div>", unsafe_allow_html=True)
        
        if spots_valides:
            html_apero = "<div class='centrage-fixe'>"
            for s in spots_valides:
                q = urllib.parse.quote(s['nom'] + " Saint-Malo")
                target_url = f"https://google.com/search?q={q}"
                html_apero += f"<div class='plage-card rect-style' style='padding:15px;'><div class='card-title-clickable' onclick=\"window.open('{target_url}', '_blank');\">{s['nom']}</div><p class='card-text'><b>{s['type']}</b><br>{s['description']}</p><b style='color:#2d5a27;'>☀️ AU SOLEIL & À L'ABRI 🍹</b></div>"
            html_apero += "</div>"
            st.markdown(html_apero, unsafe_allow_html=True)
        else:
            st.markdown("<div class='rect-style' style='padding:20px; text-align:center; color:#222;'>Aucun spot idéal trouvé à cette heure-là pour cette orientation de vent/soleil.</div>", unsafe_allow_html=True)
