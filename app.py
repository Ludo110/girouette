import streamlit as st
import requests
import urllib.parse

st.set_page_config(page_title="Girouette Malouine", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #5d7689 !important; }
    
    /* Conteneur principal pour centrer les éléments */
    .cards-container { 
        display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; margin-top: 20px; 
    }
    
    /* Style épuré pour les cartes et la météo */
    .box { 
        background-color: #e2dfd7; 
        border-radius: 15px; 
        padding: 20px; 
        box-shadow: 0 4px 8px rgba(0,0,0,0.2); 
        text-align: center;
    }
    
    .plage-card { width: 200px; height: 230px; display: flex; flex-direction: column; align-items: center; justify-content: space-between; }
    .card-title { color: #5d7689; font-size: 1.2em; text-decoration: underline; margin-bottom: 5px; }
    a { text-decoration: none !important; color: inherit; }
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

# Données météo
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
ori = dirs[int(round((angle % 360) / 45))]

# Affichage météo
st.markdown(f"<div class='box' style='max-width:400px; margin:0 auto 30px auto;'>🌬️ Vent: {vitesse} km/h - 🧭 <b>{ori} ({int(angle)}°)</b></div>", unsafe_allow_html=True)

# Logique de tri
abritees = [p for p in plages if (True if vitesse < 10 else (p["Min"] <= angle <= p["Max"] if p["Min"] <= p["Max"] else (angle >= p["Min"] or angle <= p["Max"])))]
exposees = [p for p in plages if p not in abritees]

# Affichage
st.markdown("<h3 style='color:white; text-align:center;'>🟢 À l'abri</h3>", unsafe_allow_html=True)
st.markdown("<div class='cards-container'>", unsafe_allow_html=True)
for p in abritees:
    q = urllib.parse.quote(f"{p['Nom']} {p['Ville']}")
    st.markdown(f"""
        <div class='box plage-card'>
            <a href='https://google.com/search?q={q}'>
                <div class='card-title'>{p['Nom']}</div>
                <div style='color:#555;'>{p['Ville']}</div>
            </a>
            <div style='color:#2d5a27; font-weight:bold;'>✔ ID
