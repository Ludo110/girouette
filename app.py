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

# Style de fond : Sable ultra-léger, lumineux et doux
st.html("""
<style>
    .stApp {
        background-color: #fdfbf7 !important;
    }
</style>
""")

# En-tête minimaliste et chic
st.html("""
<div style="font-family: 'Inter', sans-serif; margin-bottom: 30px; padding-left: 10px;">
    <h1 style="color: #451a03; font-size: 36px; font-weight: 800; margin-bottom: 5px;">🏖️ Girouette</h1>
    <p style="color: #7c2d12; font-size: 16px; margin: 0; opacity: 0.7;">Trouvez la plage idéale à l'abri du vent</p>
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

# Bandeau météo avec fine bordure terracotta élégante
st.html(f"""
<div style="display: flex; justify-content: flex-start; gap: 40px; align-items: center; 
            background-color: #ffffff; padding: 15px 25px; border-radius: 14px; 
            box-shadow: 0 4px 12px rgba(69, 26, 3, 0.02); border: 1px solid #f5f0eb;
            border-left: 4px solid #7c2d12;
            font-family: 'Inter', sans-serif; margin-bottom: 35px; margin-left: 10px; margin-right: 10px;">
    <div style="font-size: 16px
