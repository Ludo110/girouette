import streamlit as st
import requests

st.set_page_config(page_title="Test Direct Live", layout="centered")

st.title("Test Température Réelle en Direct (Open-Meteo Current)")

LAT_SM, LON_SM = 48.6493, -2.0089
url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT_SM}&longitude={LON_SM}&current=temperature_2m,wind_speed_10m,wind_direction_10m"

try:
    resp = requests.get(url, timeout=5)
    data = resp.json()
    st.write("Données brutes :", data)
    
    temp_actuelle = data["current"]["temperature_2m"]
    vent_actuel = data["current"]["wind_speed_10m"]
    
    st.metric("Température Actuelle Saint-Malo", f"{temp_actuelle} °C")
    st.metric("Vent Actuel", f"{vent_actuel} km/h")
except Exception as e:
    st.error(f"Erreur : {e}")
