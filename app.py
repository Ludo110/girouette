import streamlit as st
import requests
from datetime import datetime, timezone
import zoneinfo

st.set_page_config(page_title="Test Plongée & Chasse", layout="centered")

tz_france = zoneinfo.ZoneInfo("Europe/Paris")
now_france = datetime.now(tz_france)

LAT_SM, LON_SM = 48.6493, -2.0089

st.title("🤿 Bac à sable - Conditions Chasse & Plongée")

@st.cache_data(ttl=3600)
def fetch_marine_data():
    try:
        # API Marine Open-Meteo pour la houle et les vagues
        url = f"https://marine-api.open-meteo.com/v1/marine?latitude={LAT_SM}&longitude={LON_SM}&current=wave_height,wave_direction,wave_period,sea_surface_temperature"
        resp = requests.get(url, timeout=5).json()
        return resp.get("current", {})
    except Exception:
        return {}

@st.cache_data(ttl=3600)
def fetch_meteo_data():
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT_SM}&longitude={LON_SM}&current=wind_speed_10m,wind_direction_10m,precipitation"
        resp = requests.get(url, timeout=5).json()
        return resp.get("current", {})
    except Exception:
        return {}

marine = fetch_marine_data()
meteo = fetch_meteo_data()

wave_height = marine.get("wave_height", 0.5)
wave_period = marine.get("wave_period", 6.0)
sea_temp = marine.get("sea_surface_temperature", 15.0)

wind_speed = meteo.get("wind_speed_10m", 15)
wind_dir = meteo.get("wind_direction_10m", 270)
rain = meteo.get("precipitation", 0.0)

# Algorithme simple d'évaluation pour la chasse / plongée
def evaluer_conditions_chasse(v_vent, h_vague, pluie):
    if pluie > 0.5:
        return "🔴 Eaux chargées (Pluies récentes)", "Le run des rivières / ruisseaux plombe la visibilité côtière."
    if h_vague > 1.2:
        return "🔴 Trop agité (Houle forte)", "Fond brassé, visibilité nulle et risque de clapot dangereux."
    if v_vent > 25:
        return "🟠 Vent fort (Clapot de surface)", "Navigabilité et surface compliquées, visibilité dégradée."
    if h_vague < 0.5 and v_vent < 15:
        return "🟢 Top conditions (Mer d'huile)", "Excellentes dispositions pour de l'eau claire et un plan d'eau plat."
    return "🟡 Correct / Modéré", "Visibilité correcte mais vigilance selon l'orientation du spot."

statut, conseil = evaluer_conditions_chasse(wind_speed, wave_height, rain)

st.subheader("Indicateurs actuels au large de Saint-Malo")
st.markdown(f"""
- **Statut Plongée / Chasse :** **{statut}**
- *Conseil :* {conseil}
- **Hauteur des vagues :** {wave_height} m (Période : {wave_period} s)
- **Vent :** {wind_speed} km/h (Direction : {wind_dir}°)
- **Température de l'eau :** {sea_temp}°C
- **Pluie récente :** {rain} mm
""")
