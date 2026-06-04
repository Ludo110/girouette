import streamlit as st
import requests
import urllib.parse

st.set_page_config(page_title="Girouette Malouine", layout="wide")

st.markdown("""<style>
    .stApp { background-color: #5d7689 !important; }
    .plage-card { background-color: #e2dfd7; padding: 20px 10px; border-radius: 15px; text-align: center; width: 200px; height: 250px; margin: 10px auto; display: flex; flex-direction: column; justify-content: flex-start; align-items: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    a::after { content: none !important; }
</style>""", unsafe_allow_html=True)

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

# Météo
try:
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.6493&longitude=-2.0089&current=wind_speed_10m,wind_direction_10m"
    r = requests.get(url, timeout=5).json()
    auto_v = int(r["current"]["wind_speed_10m"])
    auto_a = float(r["current"]["wind_direction_10m"])
except: auto_v, auto_a = 15, 270.0

st.title("Girouette Malouine")
with st.expander("⚙️ Options"):
    m = st.checkbox("Mode manuel")
    v = st.slider("Vitesse (km/h)", 0, 80, auto_v) if m else auto_v
    a = float(st.slider("Direction (°)", 0, 360, int(auto_a))) if m else auto_a

d = ["Nord", "Nord-Est", "Est", "Sud-Est", "Sud", "Sud-Ouest", "Ouest", "Nord-Ouest", "Nord"]
st.subheader("Vent : " + str(v) + " km/h - " + d[int(round((a % 360) / 45))])

# Tri
abritees = [p for p in plages if (True if v < 10 else (p["Min"] <= a <= p["Max"] if p["Min"] <= p["Max"] else (a >= p["Min"] or a <= p["Max"])))]
exposees = [p for p in plages if p not in abritees]

st.markdown("---")
st.write("### 🟢 À l'abri")
for i in range(0, len(abritees), 4):
    cols = st.columns(4)
    for j, p in enumerate(abritees[i:i+4]):
        q = urllib.parse.quote(p['Nom'] + " " + p['Ville'])
        cols[j].markdown("<a href='https://google.com/search?q=" + q + "'><div class='plage-card'><h3>" + p['Nom'] + "</h3><p>" + p['Ville'] + "</p><b>✔ IDÉALE</b></div></a>", unsafe_allow_html=True)

st.write("### 🔴 Exposées")
for p in exposees:
    st.write("💨 " + p['Nom'] + " (" + p['Ville'] + ")")
