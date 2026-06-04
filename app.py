import pandas as pd
import requests
import streamlit as st
import urllib.parse

# Configuration
st.set_page_config(page_title="Girouette Malouine", page_icon="🏖️", layout="wide")

# CSS pour le fond bleu-gris et les rectangles crème
st.html("""
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
""")

# En-tête
st.html("""
<div style="text-align: center; margin-bottom: 30px; font-family: sans-serif;">
    <h1 style="color: #ffffff; font-size: 50px; font-weight: 300;">Girouette Malouine</h1>
    <p style="color: #e2dfd7; font-size: 20px;">Trouvez la plage idéale à l'abri du vent</p>
</div>
""")

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

# Liste plages
donnees_plages = [
    {"Nom": "Sillon", "Ville": "Saint-Malo", "Secteur": "Paramé", "Min": 45, "Max": 225},
    {"Nom": "Bon-Secours", "Ville": "Saint-Malo", "Secteur": "Remparts", "Min": 360, "Max": 180},
    {"Nom": "Port Mer", "Ville": "Cancale", "Secteur": "Cancale", "Min": 180, "Max": 360},
    {"Nom": "Chevrets", "Ville": "Saint-Coulomb", "Secteur": "St-Coulomb", "Min": 22, "Max": 202}
]

def est_abritee(p, angle, vitesse):
    if vitesse < 10.0: return True
    mn, mx = p["Min"], p["Max"]
    return (mn <= angle <= mx) if (mn <= mx) else (angle >= mn or angle <= mx)

# Tri
abritees = [p for p in donnees_plages if est_abritee(p, wind_dir, wind_speed)]
exposees = [p for p in donnees_plages if not est_abritee(p, wind_dir, wind_speed)]

# Affichage protégées
st.markdown("<h3 style='color: #ffffff; text-align: center;'>🟢 À l'abri</h3>", unsafe_allow_html=True)
cols = st.columns(max(len(abritees), 1))
for i, p in enumerate(abritees):
    with cols[i]:
        st.html(f"""
        <div class="plage-card">
            <h3 style="color: #333
