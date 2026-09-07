import streamlit as st
import requests
import urllib.parse
import json
from datetime import datetime
from pysolar.solar import get_azimuth, get_altitude

st.set_page_config(page_title="Girouette Malouine", layout="wide")

st.markdown("""
<style>
    /* Masquer le header, le footer et le menu Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp { background-color: #64978b !important; }
    div[data-testid="stExpander"] button div p { color: #f0ede6 !important; font-weight: bold !important; }
    .centrage-fixe { display: flex; flex-direction: row; justify-content: center; gap: 20px; flex-wrap: wrap; }
    .rect-style { background-color: #f0ede6; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.15); overflow: hidden; }
    .plage-card { padding: 0px 0px 15px 0px; text-align: center; width: 260px; display: flex; flex-direction: column; justify-content: flex-start; align-items: center; }
    .card-img { width: 100%; height: 140px; object-fit: cover; }
    .card-title { width: 100%; margin: 10px 0 5px 0; font-size: 1.1em; text-decoration: underline; }
    .card-text { width: 100%; color: #666; margin: 0 0 10px 0; font-size: 0.85em; }
    a::after { content: none !important; }

    /* Conteneur global centré */
    .title-wrapper {
        display: flex;
        justify-content: center;
        width: 100%;
    }

    /* Encadré principal */
    .title-box-full {
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
    }
    .title-box-full h1 {
        margin: 0 !important;
        padding: 0 !important;
        color: #436e64 !important;
        font-size: 1.35em !important;
        text-align: center !important;
    }
    .title-box-full p {
        margin: 6px 0 0 0 !important;
        padding: 0 !important;
        color: #557a70 !important;
        font-size: 0.9em !important;
        text-align: center !important;
    }

    /* Encadrés des sections */
    .title-box-section {
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
    }
    .title-box-section h3 {
        margin: 0 !important;
        padding: 0 !important;
        color: #436e64 !important;
        font-size: 1.2em !important;
        text-align: center !important;
        width: 100% !important;
    }
    
    /* Style du sélecteur d'onglets centré */
    div[data-testid="stRadio"] {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }
    div[data-testid="stRadio"] > div {
        justify-content: center;
        background-color: #f0ede6;
        padding: 8px 16px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin: 0 auto 15px auto;
    }
</style>
""", unsafe_allow_html=True)

# Données météo Open-Meteo
LAT_SM, LON_SM = 48.6493, -2.0089
try:
    r = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={LAT_SM}&longitude={LON_SM}&current=wind_speed_10m,wind_direction_10m", timeout=5).json()
    auto_v, auto_a = int(r["current"]["wind_speed_10m"]), float(r["current"]["wind_direction_10m"])
except: 
    auto_v, auto_a = 15, 270.0

dirs = ["Nord", "Nord-Est", "Est", "Sud-Est", "Sud", "Sud-Ouest", "Ouest", "Nord-Ouest", "Nord"]

# 1. En-tête principal
st.markdown("""
<div class='title-wrapper'>
    <div class='title-box-full'>
        <h1>Girouette Malouine</h1>
        <p>Météo, plages & apéros à l'abri du vent</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 2. Navigation centrée sous le titre
onglet = st.radio("", ["🏖️ Plages", "🍹 Apéro au Soleil"], horizontal=True)

# -----------------------------------------------------------------------------
# ONGLET 1 : PLAGES
# -----------------------------------------------------------------------------
if onglet == "🏖️ Plages":
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

    with st.expander("Options"):
        if st.button("🔄 Rafraîchir les données météo", use_container_width=True):
            st.rerun()
        use_manual = st.checkbox("Activer le mode manuel")
        vitesse = st.slider("Vitesse vent (km/h)", 0, 80, auto_v) if use_manual else auto_v
        angle = float(st.slider("Direction vent ( deg )", 0, 360, int(auto_a))) if use_manual else auto_a

    ori = dirs[int(round((angle % 360) / 45))]
    st.markdown(f"<div class='rect-style' style='padding:12px; text-align:center; max-width:400px; margin:15px auto 25px auto; color:#333;'>Vent: {vitesse} km/h - {ori} ({int(angle)} deg)</div>", unsafe_allow_html=True)

    abritees = [p for p in plages if (True if vitesse < 10 else (p["Min"] <= angle <= p["Max"] if p["Min"] <= p["Max"] else (angle >= p["Min"] or angle <= p["Max"])))]
    exposees = [p for p in plages if p not in abritees]

    st.markdown("<div class='title-box-section' style='margin-bottom: 20px;'><h3>A l'abri</h3></div>", unsafe_allow_html=True)
    html_a = "<div class='centrage-fixe'>"
    for p in abritees:
        q = urllib.parse.quote(p['Nom'] + " " + p['Ville'])
        img_url = f"https://raw.githubusercontent.com/Ludo110/girouette/main/{p['Image']}"
        palmier_url = f"https://raw.githubusercontent.com/Ludo110/girouette/main/Palmier.png"
        html_a += f"<div class='plage-card rect-style'><img src='{img_url}' class='card-img' onerror=\"this.src='{palmier_url}';\"><a href='https://google.com/search?q={q}' style='text-decoration:none;'><h3 class='card-title' style='color: #436e64;'>{p['Nom']}</h3></a><p class='card-text'>{p['Ville']}</p><b style='color:#2d5a27;'>IDEALE</b></div>"
    html_a += "</div>"
    st.markdown(html_a, unsafe_allow_html=True)

    st.markdown("<div class='title-box-section' style='margin-top: 30px; margin-bottom: 20px;'><h3>Exposées</h3></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    milieu = len(exposees) // 2

    def afficher_colonne(liste_plages, colonne):
        with colonne:
            for p in liste_plages:
                q = urllib.parse.quote(p['Nom'] + " " + p['Ville'])
                st.markdown(f"<div style='text-align:center; margin-bottom:10px;'><a href='https://google.com/search?q={q}' style='color:white;'>{p['Nom']} ({p['Ville']})</a></div>", unsafe_allow_html=True)

    afficher_colonne(exposees[:milieu], col1)
    afficher_colonne(exposees[milieu:], col2)

# -----------------------------------------------------------------------------
# ONGLET 2 : APÉRO AU SOLEIL
# -----------------------------------------------------------------------------
elif onglet == "🍹 Apéro au Soleil":
    # Calcul de la position du soleil
    now = datetime.utcnow()
    sol_alt = get_altitude(LAT_SM, LON_SM, now)
    sol_azi = get_azimuth(LAT_SM, LON_SM, now)

    with st.expander("Options"):
        if st.button("🔄 Rafraîchir les données", use_container_width=True):
            st.rerun()
        use_manual = st.checkbox("Activer le mode manuel (Apéro)")
        vitesse = st.slider("Vitesse vent (km/h)", 0, 80, auto_v) if use_manual else auto_v
        angle = float(st.slider("Direction vent ( deg )", 0, 360, int(auto_a))) if use_manual else auto_a

    ori = dirs[int(round((angle % 360) / 45))]
    st.markdown(f"<div class='rect-style' style='padding:12px; text-align:center; max-width:420px; margin:15px auto 25px auto; color:#333;'>Météo : Vent {vitesse} km/h ({ori}) — Soleil : Alt {int(sol_alt)}° / Azi {int(sol_azi)}°</div>", unsafe_allow_html=True)

    # Chargement des spots
    try:
        with open("spots_apero.json", "r", encoding="utf-8") as f:
            spots = json.load(f)
    except Exception as e:
        st.error("Impossible de charger spots_apero.json")
        spots = []

    # Filtrage
    spots_valides = []
    if sol_alt <= 2:
        st.markdown("<div class='rect-style' style='padding:20px; text-align:center; color:#333;'><b>🌙 Le soleil est couché ! Rendez-vous demain pour l'apéro.</b></div>", unsafe_allow_html=True)
    else:
        for s in spots:
            # Check soleil
            au_soleil = (s["soleil_azimut_min"] <= sol_azi <= s["soleil_azimut_max"])
            # Check vent
            abrite_vent = True if vitesse < 10 else (ori in s["vents_abrites"])
            
            if au_soleil and abrite_vent:
                spots_valides.append(s)

        st.markdown("<div class='title-box-section' style='margin-bottom: 20px;'><h3>Top Spots Apéro</h3></div>", unsafe_allow_html=True)
        
        if spots_valides:
            html_apero = "<div class='centrage-fixe'>"
            for s in spots_valides:
                q = urllib.parse.quote(s['nom'] + " Saint-Malo")
                html_apero += f"<div class='plage-card rect-style' style='padding:15px;'><a href='https://google.com/search?q={q}' style='text-decoration:none;'><h3 class='card-title' style='color: #436e64;'>{s['nom']}</h3></a><p class='card-text'><b>{s['type']}</b><br>{s['description']}</p><b style='color:#2d5a27;'>☀️ AU SOLEIL & À L'ABRI 🍹</b></div>"
            html_apero += "</div>"
            st.markdown(html_apero, unsafe_allow_html=True)
        else:
            st.markdown("<div class='rect-style' style='padding:20px; text-align:center; color:#333;'>Aucun spot idéal trouvé actuellement pour cette orientation de vent/soleil.</div>", unsafe_allow_html=True)
