import pandas as pd
import requests
import streamlit as st
import urllib.parse

# Configuration
st.set_page_config(page_title="Girouette Malouine", page_icon="🏖️", layout="wide")

# Style : Fond bleu-gris et style des rectangles crème
st.markdown("""
<style>
    .stApp { background-color: #5d7689 !important; }
    .plage-card {
        background-color: #e2dfd7;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        height: 200px;
        margin: 10px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
</style>
""", unsafe_allow_html=True)

# En-tête
st.markdown("""
<div style="text-align: center; margin-bottom: 30px; font-family: sans-serif;">
    <h1 style="color: #ffffff; font-size: 50px; font-weight: 300;">Girouette Malouine</h1>
    <p style="color: #e2dfd7; font-size: 20px;">Trouvez la plage idéale à l'abri du vent</p>
</div>
""", unsafe_allow_html=True)

# Météo
def get_current_wind():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=48.6493&longitude=-2.0089&current=wind_speed_10m,wind_direction_10m&timezone=Europe%2FParis"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return float(data["current"]["wind_direction_10m"]), float(data["current"]["wind_speed_10m"])
    except: pass
    return 270.0, 15.0

wind_dir, wind_speed = get_current_wind()

# Bandeau météo
directions_texte = ["Nord", "Nord-Est", "Est", "Sud-Est", "Sud", "Sud-Ouest", "Ouest", "Nord-Ouest", "Nord"]
index_dir = int(round(((wind_dir % 360) / 45)))
vent_cardinal = directions_texte[index_dir]

st.markdown(f"""
<div style="text-align: center; background-color: #e2dfd7; padding: 15px; border-radius: 12px; margin-bottom: 30px; font-family: sans-serif; color: #333;">
    🌬️ <b>Vent :</b> {vent_cardinal} ({int(wind_dir)}°) | 🚀 <b>Vitesse :</b> {int(wind_speed)} km/h
</div>
""", unsafe_allow_html=True)

# Liste complète
donnees_plages = [
    {"Nom": "La Passagère", "Ville": "Saint-Malo", "Secteur": "St-Servan", "Min": 315, "Max": 135},
    {"Nom": "Fours à Chaux", "Ville": "Saint-Malo", "Secteur": "St-Servan", "Min": 315, "Max": 135},
    {"Nom": "Saint-Père", "Ville": "Saint-Malo", "Secteur": "Solidor", "Min": 315, "Max": 135},
    {"Nom": "Les Sablons", "Ville": "Saint-Malo", "Secteur": "St-Servan", "Min": 45, "Max": 225},
    {"Nom": "Bon-Secours", "Ville": "Saint-Malo", "Secteur": "Remparts", "Min": 360, "Max": 180},
    {"Nom": "L'Éventail", "Ville": "Saint-Malo", "Secteur": "Remparts", "Min": 360, "Max": 180},
    {"Nom": "Le Sillon", "Ville": "Saint-Malo", "Secteur": "Paramé", "Min": 45, "Max": 225},
    {"Nom": "Le Val", "Ville": "Rothéneuf", "Secteur": "Rothéneuf", "Min": 45, "Max": 225},
    {"Nom": "Les Chevrets", "Ville": "Saint-Coulomb", "Secteur": "St-Coulomb", "Min": 22, "Max": 202},
    {"Nom": "La Touesse", "Ville": "Saint-Coulomb", "Secteur": "St-Coulomb", "Min": 90, "Max": 270},
