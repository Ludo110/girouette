import streamlit as st
import requests
import urllib.parse

# 1. Configuration et Style
st.set_page_config(page_title="Girouette Malouine", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #5d7689 !important; }
    .plage-card { background-color: #e2dfd7; padding: 20px; border-radius: 15px; text-align: center; height: 180px; margin: 10px; display: flex; flex-direction: column; justify-content: center; }
</style>
""", unsafe_allow_html=True)

# 2. En-tête et Météo
st.markdown("<h1 style='color: white; text-align: center;'>Girouette Malouine</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #e2dfd7; text-align: center;'>Trouvez la plage idéale à l'abri du vent</p>", unsafe_allow_html=True)

try:
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.6493&longitude=-2.0089&current=wind_speed_10m,wind_direction_10m"
    data = requests.get(url, timeout=5).json()
    vitesse, angle = int(data["current"]["wind_speed_10m"]), data["current"]["wind_direction_10m"]
except: vitesse, angle = 15, 270

st.markdown(f"<div style='background:#e2dfd7; padding:15px; border-radius:10px; text-align:center; max-width: 400px; margin: 0 auto 30px auto;'>🌬️ Vent: {vitesse} km/h - Direction: {angle}°</div>", unsafe_allow_html=True)

# 3. Liste des plages
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

# 4. Tri
abritees = [p for p in plages if (True if vitesse < 10 else (p["Min"] <= angle <= p["Max"] if p["Min"] <= p["Max"] else (angle >= p["Min"] or angle <= p["Max"])))]
exposees = [p for p in plages if p not in abritees]

# 5. Affichage centré
st.markdown("<h3 style='color: white; text-align: center;'>🟢 À l'abri</h3>", unsafe_allow_html=True)

# Créer des colonnes centrées dynamiquement
num_abritees = len(abritees)
if num_abritees > 0:
    # On limite à 4 colonnes max par ligne
    cols_count = min(num_abritees, 4)
    # Pour centrer : on crée des colonnes vides autour si besoin
    cols = st.columns(cols_count)
    for i, p in enumerate(abritees):
        query = urllib.parse.quote(f"{p['Nom']} {p['Ville']}")
        cols[i % 4].markdown(f"""
        <a href='https://www.google.com/maps/search/{query}' style='text-decoration:none;'>
            <div class='plage-card'>
                <h3 style='color:#333; margin:0;'>{p['Nom']}</h3>
                <p style='color:#555;'>{p['Ville']}</p>
                <b style='color:#2d5a27;'>✔ IDÉALE</b>
            </div>
        </a>""", unsafe_allow_html=True)

st.markdown("<h3 style='color: #e2dfd7; text-align: center; margin-top: 40px;'>🔴 Exposées</h3>", unsafe_allow_html=True)
for p in exposees:
    query = urllib.parse.quote(f"{p['Nom']} {p['Ville']}")
    st.markdown(f"<div style='text-align: center;'><a href='https://www.google.com/maps/search/{query}' style='color:white;'>💨 {p['Nom']} ({p['Ville']})</a></div>", unsafe_allow_html=True)
