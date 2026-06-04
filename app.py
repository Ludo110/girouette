import streamlit as st
import requests
import urllib.parse
st.set_page_config(page_title="Girouette Malouine", layout="wide")
st.markdown("""<style>
.stApp { background-color: #5d7689 !important; }
.st-expander, .st-expander div[role="button"], .st-expander p { color: #e2dfd7 !important; font-weight: bold; }
.centrage-fixe { display: flex; flex-direction: row; justify-content: center; gap: 20px; flex-wrap: wrap; }
.rect-style { background-color: #e2dfd7; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.2); }
.plage-card { padding: 20px 10px; text-align: center; width: 200px; height: 250px; display: flex; flex-direction: column; justify-content: flex-start; align-items: center; }
.card-title { width: 100%; margin: 0 0 10px 0; font-size: 1.2em; text-decoration: underline; }
.card-text { width: 100%; color: #555; margin: 0 0 10px 0; font-size: 0.9em; }
a::after { content: none !important; }
</style>""", unsafe_allow_html=True)
plages = [{"Nom": "La Passagère", "Ville": "Saint-Malo", "Min": 315, "Max": 135}, {"Nom": "Fours à Chaux", "Ville": "Saint-Malo", "Min": 315, "Max": 135}, {"Nom": "Saint-Père", "Ville": "Saint-Malo", "Min": 315, "Max": 135}, {"Nom": "Les Sablons", "Ville": "Saint-Malo", "Min": 45, "Max": 225}, {"Nom": "Bon-Secours", "Ville": "Saint-Malo", "Min": 360, "Max": 180}, {"Nom": "L'Éventail", "Ville": "Saint-Malo", "Min": 360, "Max": 180}, {"Nom": "Le Sillon", "Ville": "Saint-Malo", "Min": 45, "Max": 225}, {"Nom": "Le Val", "Ville": "Rothéneuf", "Min": 45, "Max": 225}, {"Nom": "Les Chevrets", "Ville": "Saint-Coulomb", "Min": 22, "Max": 202}, {"Nom": "La Touesse", "Ville": "Saint-Coulomb", "Min": 90, "Max": 270}, {"Nom": "Le Guesclin", "Ville": "Saint-Coulomb", "Min": 45, "Max": 225}, {"Nom": "Le Verger", "Ville": "Saint-Coulomb", "Min": 45, "Max": 225}, {"Nom": "Port Mer", "Ville": "Cancale", "Min": 180, "Max": 360}]
try:
    r = requests.get("https://api.open-meteo.com/v1/forecast?latitude=48.6493&longitude=-2.0089&current=wind_speed_10m,wind_direction_10m", timeout=5).json()
    auto_v, auto_a = int(r["current"]["wind_speed_10m"]), float(r["current"]["wind_direction_10m"])
except: auto_v, auto_a = 15, 270.0
st.markdown("<h1 style='color: white; text-align: center;'>Girouette Malouine</h1>", unsafe_allow_html=True)
with st.expander("⚙️ Options"):
    use_manual = st.checkbox("Activer le mode manuel")
    vitesse = st.slider("Vitesse vent (km/h)", 0, 80, auto_v) if use_manual else auto_v
    angle = float(st.slider("Direction vent (°)", 0, 360, int(auto_a))) if use_manual else auto_a
dirs = ["Nord", "Nord-Est", "Est", "Sud-Est", "Sud", "Sud-Ouest", "Ouest", "Nord-Ouest", "Nord"]
ori = dirs[int(round((angle % 360) / 45))]
st.markdown(f"<div class='rect-style' style='padding:15px; text-align:center; max-width:400px; margin:0 auto 30px auto;'>🌬️ Vent: {vitesse} km/h - 🧭 <b>{ori} ({int(angle)}°)</b></div>", unsafe_allow_html=True)
abritees = [p for p in plages if (True if vitesse < 10 else (p["Min"] <= angle <= p["Max"] if p["Min"] <= p["Max"] else (angle >= p["Min"] or angle <= p["Max"])))]
exposees = [p for p in plages if p not in abritees]
st.markdown("<h3 style='color:white; text-align:center;'>🟢 À l'abri</h3>", unsafe_allow_html=True)
html_a = "<div class='centrage-fixe'>"
for p in abritees:
    q = urllib.parse.quote(p['Nom'] + " " + p['Ville'])
    html_a += f"<div class='plage-card rect-style'><a href='https://google.com/search?q={q}' style='text-decoration:none;'><h3 class='card-title' style='color: #5d7689;'>{p['Nom']}</h3></a><p class='card-text'>{p['Ville']}</p><b style='color:#2d5a27;'>✔ IDÉALE</b></div>"
html_a += "</div>"
st.markdown(html_a, unsafe_allow_html=True)
st.markdown("<h3 style='color:#e2dfd7; text-align:center; margin-top:40px;'>🔴 Exposées</h3>", unsafe_allow_html=True)
for p in exposees:
    q = urllib.parse.quote(p['Nom'] + " " + p['Ville'])
    st.markdown(f"<div style='text-align:center;'><a href='https://google.com/search?q={q}' style='color:white;'>💨 {p['Nom']} ({p['Ville']})</a></div>", unsafe_allow_html=True)
