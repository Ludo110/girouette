import streamlit as st
import requests
import urllib.parse

# 1. Configuration et Style
st.set_page_config(page_title="Girouette Malouine", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #5d7689 !important; }
    .plage-card { background-color: #e2dfd7; padding: 20px; border-radius: 15px; text-align: center; height: 180px; margin: 10px; }
</style>
""", unsafe_allow_html=True)

# 2. Titre et Météo
st.markdown("<h1 style='color: white; text-align: center;'>Girouette Malouine</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #e2dfd7; text-align: center;'>Trouvez la plage idéale</p>", unsafe_allow_html=True)

try:
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.6493&longitude=-2.0089&current=wind_speed_10m,wind_direction_10m"
    data = requests.get(url, timeout=5).json()
    vitesse = int(data["current"]["wind_speed_10m"])
    angle = data["current"]["wind_direction_10m"]
except:
    vitesse, angle = 15, 270

st.markdown(f"<div style='background:#e2dfd7; padding:10px; border-radius:10px; text-align:center;'>Vent: {vitesse} km/h - Angle: {angle}°</div>", unsafe_allow_html=True)

# 3. Données
plages = [
    {"Nom": "Sillon", "Ville": "Saint-Malo", "Min": 45, "Max": 225},
    {"Nom": "Bon-Secours", "Ville": "Saint-Malo", "Min": 360, "Max": 180},
    {"Nom": "Port Mer", "Ville": "Cancale", "Min": 180, "Max": 360},
    {"Nom": "Chevrets", "Ville": "Saint-Coulomb", "Min": 22, "Max": 202}
]

# 4. Logique et Affichage
abritees = []
exposees = []
for p in plages:
    est_ok = True if vitesse < 10 else (p["Min"] <= angle <= p["Max"] if p["Min"] <= p["Max"] else (angle >= p["Min"] or angle <= p["Max"]))
    if est_ok: abritees.append(p)
    else: exposees.append(p)

st.subheader("🟢 À l'abri")
cols = st.columns(4)
for i, p in enumerate(abritees):
    with cols[i % 4]:
        query = urllib.parse.quote(f"{p['Nom']} {p['Ville']}")
        st.markdown(f"""
        <a href='http://google.com/search?q={query}' style='text-decoration:none;'>
            <div class='plage-card'>
                <h3 style='color:#333;'>{p['Nom']}</h3>
                <p style='color:#555;'>{p['Ville']}</p>
                <b style='color:green;'>✔ IDÉALE</b>
            </div>
        </a>""", unsafe_allow_html=True)

st.subheader("🔴 Exposées")
for p in exposees:
    st.markdown(f"<div style='color:white;'>💨 {p['Nom']} ({p['Ville']})</div>", unsafe_allow_html=True)
