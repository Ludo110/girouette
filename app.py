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

# 2. En-tête
st.markdown("<h1 style='color: white; text-align: center;'>Girouette Malouine</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #e2dfd7; text-align: center;'>Trouvez la plage idéale à l'abri du vent</p>", unsafe_allow_html=True)

# Récupération automatique
try:
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.6493&longitude=-2.0089&current=wind_speed_10m,wind_direction_10m"
    data = requests.get(url, timeout=5).json()
    auto_vitesse, auto_angle = int(data["current"]["wind_speed_10m"]), data["current"]["wind_direction_10m"]
except:
    auto_vitesse, auto_angle = 15, 270

# 3. Options manuelles (Expander)
with st.expander("⚙️ Mode Manuel (Forcer les conditions)"):
    use_manual = st.checkbox("Activer le mode manuel")
    man_vitesse = st.slider("Vitesse du vent (km/h)", 0, 80, auto_vitesse)
    man_angle = st.slider("Direction du vent (°)", 0, 360, int(auto_angle))

vitesse = man_vitesse if use_manual else auto_vitesse
angle = float(man_angle if use_manual else auto_angle)

# Affichage météo
directions = ["Nord", "Nord-Est", "Est", "Sud-Est", "Sud", "Sud-Ouest", "Ouest", "Nord-Ouest", "Nord"]
orientation = directions[int(round((angle % 360) / 45))]

st.markdown(f"""
<div style='background:#e2dfd7; padding:15px; border-radius:10px; text-align:center; max-width: 400px; margin: 0 auto 30px auto;'>
    🌬️ Vent: {vitesse} km/h - 🧭 <b>{orientation} ({int(angle)}°)</b>
</div>
""", unsafe_allow_html=True)

# 4. Données
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

# 5. Tri et Affichage
abritees = []
exposees = []
for p in plages:
    est_ok = True if vitesse < 10 else (p["Min"] <= angle <= p["Max"] if p["Min"] <= p["Max"] else (angle >= p["Min"] or angle <= p["Max"]))
    if est_ok: abritees.append(p)
    else: exposees.append(p)

st.markdown("<h3 style='color: white; text-align: center;'>🟢 À l'abri</h3>", unsafe_allow_html=True)

if abritees:
    for i in range(0, len(abritees), 4):
        groupe = abritees[i:i+4]
        cols = st.columns(len(groupe))
        for j, p in enumerate(groupe):
            query = urllib.parse.quote(f"{p['Nom']} {p['Ville']}")
            cols[j].markdown(f"""
            <a href='http://google.com/search?q={query}' style='text-decoration:none;'>
                <div class='plage-card'>
                    <h3 style='color:#333; margin:0;'>{p['Nom']}</h3>
                    <p style='color:#555;'>{p['Ville']}</p>
                    <b style='color:#2d5a27;'>✔ IDÉALE</b>
                </div>
            </a>""", unsafe_allow_html=True)

st.markdown("<h3 style='color: #e2dfd7; text-align: center; margin-top: 40px;'>🔴 Exposées</h3>", unsafe_allow_html=True)
for p in exposees:
    query = urllib.parse.quote(f"{p['Nom']} {p['Ville']}")
    st.markdown(f"<div style='text-align: center;'><a href='http://google.com/search?q={query}' style='color:white;'>💨 {p['Nom']} ({p['Ville']})</a></div>", unsafe_allow_html=True)
