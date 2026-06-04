import streamlit as st
import requests
import urllib.parse

st.set_page_config(page_title="Girouette Malouine", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #5d7689 !important; }
    .plage-card { background-color: #e2dfd7; padding: 20px 10px; border-radius: 15px; text-align: center; width: 200px; height: 250px; margin: 10px auto; display: flex; flex-direction: column; justify-content: flex-start; align-items: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .card-title { width: 100%; color: #333; margin: 0 0 10px 0; font-size: 1.2em; text-decoration: underline; }
    .card-text { width: 100%; color: #555; margin: 0 0 10px 0; font-size: 0.9em; }
    a::after { content: none !important; }
    [data-testid='column'] { display: flex; justify-content: center; }
</style>
""", unsafe_allow_html=True)

plages = [
    {"Nom": "La Passagère", "Ville": "Saint-Malo", "Min": 315, "Max": 135},
    {"Nom": "Fours à Chaux", "Ville": "Saint-Malo", "Min": 315, "Max": 135},
    {"Nom": "Saint-Père", "Ville": "Saint-Malo", "Min": 315, "Max": 135},
    {"Nom": "Les Sablons", "Ville": "Saint-Malo", "Min": 45, "Max": 225},
    {"Nom": "Bon-Secours", "Ville": "Saint-Malo", "Min": 360, "Max": 180},
    {"Nom": "L'Éventail", "Ville": "Saint-Malo", "Min": 360, "Max": 180},
    {"Nom": "Le Sillon", "Ville": "Saint-Malo", "Min": 45, "Max": 225},
    {"Nom": "Le Val", "Ville": "Rothéneuf", "Min": 45, "Max": 225},
    {"Nom": "Les Chevrets", "Ville": "Saint-Coulomb", "Min": 22, "Max": 202},
    {"Nom": "La Touesse", "Ville": "Saint-Coulomb", "Min": 90, "Max": 270},
    {"Nom": "Le Guesclin", "Ville": "Saint-Coulomb", "Min": 45, "Max": 225},
    {"Nom": "Le Verger", "Ville": "Saint-Coulomb", "Min": 45, "Max": 225},
    {"Nom": "Port Mer", "Ville": "Cancale", "Min": 180, "Max": 360}
]

try:
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.6493&longitude=-2.0089&current=wind_speed_10m,wind_direction_10m"
    data = requests.get(url, timeout=5).json()
    auto_v = int(data["current"]["wind_speed_10m"])
    auto_a = float(data["current"]["wind_direction_10m"])
except:
    auto_v, auto_a = 15, 270.0

st.markdown("<h1 style='color: white; text-align: center;'>Girouette Malouine</h1>", unsafe_allow_html=True)

with st.expander("⚙️ Options"):
    use_manual = st.checkbox("Activer le mode manuel")
    vitesse = st.slider("Vitesse vent (km/h)", 0, 80, auto_v) if use_manual else auto_v
    angle = float(st.slider("Direction vent (°)", 0, 360, int(auto_a))) if use_manual else auto_a

dirs = ["Nord", "Nord-Est", "Est", "Sud-Est", "Sud", "Sud-Ouest", "Ouest", "Nord-Ouest", "Nord"]
ori = dirs[int(round((angle % 360) /
