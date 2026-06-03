import streamlit as st
import pandas as pd
import requests
import urllib.parse

# 1. Configuration de la page en mode LARGE pour la grille
st.set_page_config(
    page_title="Girouette - Abri Plages", 
    page_icon="🏖️",
    layout="wide"
)

# Style de fond : Le bleu-vert canard exact (#568E94)
st.html("""
<style>
    .stApp {
        background-color: #568E94 !important;
    }
</style>
""")

# En-tête (Texte blanc et crème pour ressortir sur le fond coloré)
st.html("""
<div style="font-family: 'Inter', sans-serif; margin-bottom: 30px; padding-left: 10px;">
    <h1 style="color: #ffffff; font-size: 36px; font-weight: 800; margin-bottom: 5px; text-shadow: 0 1px 2px rgba(0,0,0,0.1);">🏖️ Girouette</h1>
    <p style="color: #ffedd5; font-size: 16px; margin: 0; opacity: 0.9;">Trouvez la plage idéale à l'abri du vent</p>
</div>
""")

# 2. Récupération de la météo en direct
def get_current_wind():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=48.6493&longitude=-2.0089&current=wind_speed_10m,wind_direction_10m&timezone=Europe%2FParis"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return float(data['current']['wind_direction_10m']), float(data['current']['wind_speed_10m'])
    except Exception:
        pass
    return 270.0, 15.0

wind_dir, wind_speed = get_current_wind()

# Options et Mode Manuel
with st.expander("⚙️ Options et Mode Manuel"):
    auto_mode = st.checkbox("Utiliser la météo en direct", value=True)
    if not auto_mode:
        wind_dir = st.slider("Direction du vent (degrés)", 0, 360, int(wind_dir))
        wind_speed = st.slider("Vitesse du vent (km/h)", 0, 80, int(wind_speed))

# Calcul de la direction du vent
directions_texte = ["Nord ⬇️", "Nord-Est ↙️", "Est ⬅️", "Sud-Est ↖️", "Sud ⬆️", "Sud-Ouest ↗️", "Ouest ➡️", "Nord-Ouest ↘️", "Nord ⬇️"]
index_dir = int(round(((wind_dir % 360) / 45)))
vent_cardinal = directions_texte[index_dir]

# Bandeau météo en couleur #dde2c5
st.html(f"""
<div style="display: flex; justify-content: flex-start; gap: 40px; align-items: center; 
            background-color: #dde2c5; padding: 15px 25px; border-radius: 14px; 
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05); border: 1px solid rgba(255,255,255,0.1);
            border-left: 5px solid #ffedd5;
            font-family: 'Inter', sans-serif; margin-bottom: 35px; margin-left: 10px; margin-right: 10px;">
    <div style="font-size: 16px; color: #ffffff; font-weight: 500;">
        🌬️ Vent actuel : <span style="font-weight: 700; color: #ffedd5;">{vent_cardinal} ({int(wind_dir)}°)</span>
    </div>
    <div style="border-left: 1px solid rgba(255,255,255,0.2); height: 25px;"></div>
    <div style="font-size: 16px; color: #ffffff; font-weight: 500;">
        🚀 Vitesse : <span style="font-weight: 700; color: #ffedd5;">{int(wind_speed)} km/h</span>
    </div>
</div>
""")

# 3. Base de données des plages
donnees_plages =
