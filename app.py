import streamlit as st
import requests
import urllib.parse

# 1. Configuration et Style
st.set_page_config(page_title="Girouette Malouine", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #5d7689 !important; }
    .plage-card { 
        background-color: #e2dfd7; 
        padding: 20px; 
        border-radius: 15px; 
        text-align: center; 
        width: 100%; 
        height: 200px; 
        display: flex; 
        flex-direction: column; 
        justify-content: center; 
        align-items: center; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 2. Données
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

# 3. Météo
try:
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.6493&longitude=-2.0089&current=wind_speed_10m,wind_direction_10m"
    data = requests.get(url, timeout=5).json()
    auto_v, auto_a = int(data["current"]["wind_speed_10m"]), float(data["current"]["wind_direction_10m"])
except: auto_v, auto_a = 15, 270.0

st.markdown("<h1 style='color: white; text-align: center;'>Girouette Malouine</h1>", unsafe_allow_html=True)

with st.expander("⚙️ Options et réglage manuel du vent"):
    use_manual = st.checkbox("Activer le mode manuel")
    vitesse = st.slider("Vitesse (km/h)", 0, 80, auto_v) if use_manual else auto_v
    angle = float(st.slider("Direction (°)", 0, 360, int(auto_a))) if use_manual else auto_a

dirs = ["Nord", "Nord-Est", "Est", "Sud-Est", "Sud", "Sud-Ouest", "Ouest", "Nord-Ouest", "Nord"]
ori = dirs[int(round((angle % 360) / 45))]
st.markdown("<div style='background:#e2dfd7; padding:15px; border-radius:10px; text-align:center; max-width:400px; margin:0 auto 30px auto;'>🌬️ Vent: " + str(vitesse) + " km/h - 🧭 <b>" + ori + " (" + str(int(angle)) + "°)</b></div>", unsafe_allow_html=True)

# 4. Tri et Affichage
abritees = [p for p in plages if (True if vitesse < 10 else (p["Min"] <= angle <= p["Max"] if p["Min"] <= p["Max"] else (angle >= p["Min"] or angle <= p["Max"])))]
exposees = [p for p in plages if p not in abritees]

st.markdown("<h3 style='color:white; text-align:center;'>🟢 À l'abri</h3>", unsafe_allow_html=True)

# Découpage en colonnes pour garder la disposition horizontale
for i in range(0, len(abritees), 4):
    ligne = abritees[i:i+4]
    cols = st.columns(4)
    for j, p in enumerate(ligne):
        q = urllib.parse.quote(p['Nom'] + " " + p['Ville'])
        cols[j].markdown(
            "<a href='https://google.com/search?q=" + q + "' style='text-decoration:none;'>"
            "<div class='plage-card'>"
            "<h3 style='color:#333; margin:0;'>" + p['Nom'] + "</h3>"
            "<p style='color:#555; margin:5px 0 0 0;'>" + p['Ville'] + "</p>"
            "<b style='color:#2d5a27;'>✔ IDÉALE</b>"
            "</div></a>", unsafe_allow_html=True)

st.markdown("<h3 style='color:#e2dfd7; text-align:center; margin-top:40px;'>🔴 Exposées</h3>", unsafe_allow_html=True)
for p in exposees:
    q = urllib.parse.quote(p['Nom'] + " " + p['Ville'])
    st.markdown("<div style='text-align:center;'><a href='https://google.com/search?q=" + q + "' style='color:white;'>💨 " + p['Nom'] + " (" + p['Ville'] + ")</a></div>", unsafe_allow_html=True)
