import streamlit as st
import requests
import urllib.parse

# 1. Configuration
st.set_page_config(page_title="Girouette Malouine", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #5d7689 !important; }
    .plage-card { background-color: #e2dfd7; padding: 20px; border-radius: 15px; text-align: center; height: 180px; margin: 10px; display: flex; flex-direction: column; justify-content: center; }
</style>
""", unsafe_allow_html=True)

# 2. Données et Météo
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
except: auto_v, auto_a = 15, 270.0

# 3. Interface simple pour rafraîchir le calcul immédiatement
st.markdown("<h1 style='color: white; text-align: center;'>Girouette Malouine</h1>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
vitesse = c1.slider("Vitesse vent (km/h)", 0, 80, auto_v)
angle = float(c2.slider("Direction vent (°)", 0, 360, int(auto_a)))

directions = ["Nord", "Nord-Est", "Est", "Sud-Est", "Sud", "Sud-Ouest", "Ouest", "Nord-Ouest", "Nord"]
ori = directions[int(round((angle % 360) / 45))]

st.markdown(f"<div style='background:#e2dfd7; padding:15px; border-radius:10px; text-align:center;'>Vent: {vitesse} km/h - 🧭 <b>{ori} ({int(angle)}°)</b></div>", unsafe_allow_html=True)

# 4. Calcul et Affichage
abritees = []
exposees = []
for p in plages:
    est_ok = True if vitesse < 10 else (p["Min"] <= angle <= p["Max"] if p["Min"] <= p["Max"] else (angle >= p["Min"] or angle <= p["Max"]))
    if est_ok: abritees.append(p)
    else: exposees.append(p)

st.markdown("<h3 style='color:white; text-align:center;'>🟢 À l'abri</h3>", unsafe_allow_html=True)
for i in range(0, len(abritees), 4):
    cols = st.columns(4)
    for j, p in enumerate(abritees[i:i+4]):
        q = urllib.parse.quote(f"{p['Nom']} {p['Ville']}")
        cols[j].markdown(f"<a href='https://google.com/search?q={q}' style='text-decoration:none;'><div class='plage-card'><h3 style='color:#333; margin:0;'>{p['Nom']}</h3><p style='color:#555;'>{p['Ville']}</p><b style='color:#2d5a27;'>✔ IDÉALE</b></div></a>", unsafe_allow_html=True)

st.markdown("<h3 style='color:#e2dfd7; text-align:center; margin-top:40px;'>🔴 Exposées</h3>", unsafe_allow_html=True)
for p in exposees:
    q = urllib.parse.quote(f"{p['Nom']} {p['Ville']}")
    st.markdown(f"<div style='text-align:center;'><a href='https://google.com/search?q={q}' style='color:white;'>💨 {p['Nom']} ({p['Ville']})</a></div>", unsafe_allow_html=True)
