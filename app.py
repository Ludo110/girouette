import pandas as pd
import requests
import streamlit as st
import urllib.parse

# 1. Configuration de la page en mode LARGE
st.set_page_config(page_title="Girouette - Abri Plages", page_icon="🏖️", layout="wide")

# Style de fond : Le bleu-vert canard exact (#568E94)
st.html("""
<style>
    .stApp {
        background-color: #568E94 !important;
    }
</style>
""")

# En-tête
st.html("""
<div style="font-family: 'Inter', sans-serif; margin-bottom: 30px; padding-left: 10px;">
    <h1 style="color: #ffffff; font-size: 36px; font-weight: 800; margin-bottom: 5px; text-shadow: 0 1px 2px rgba(0,0,0,0.1);">🏖️ Girouette Malouine</h1>
    <p style="color: #ffedd5; font-size: 16px; margin: 0; opacity: 0.9;">Trouvez la plage idéale à l'abri du vent</p>
</div>
""")

# 2. Récupération de la météo
def get_current_wind():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=48.6493&longitude=-2.0089&current=wind_speed_10m,wind_direction_10m&timezone=Europe%2FParis"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return float(data["current"]["wind_direction_10m"]), float(data["current"]["wind_speed_10m"])
    except Exception:
        pass
    return 270.0, 15.0

wind_dir, wind_speed = get_current_wind()

with st.expander("⚙️ Options et Mode Manuel"):
    auto_mode = st.checkbox("Utiliser la météo en direct", value=True)
    if not auto_mode:
        wind_dir = st.slider("Direction du vent (degrés)", 0, 360, int(wind_dir))
        wind_speed = st.slider("Vitesse du vent (km/h)", 0, 80, int(wind_speed))

directions_texte = ["Nord ⬇️", "Nord-Est ↙️", "Est ⬅️", "Sud-Est ↖️", "Sud ⬆️", "Sud-Ouest ↗️", "Ouest ➡️", "Nord-Ouest ↘️", "Nord ⬇️"]
index_dir = int(round(((wind_dir % 360) / 45)))
vent_cardinal = directions_texte[index_dir]

# Bandeau météo
st.html(f"""
<div style="background-color: #ffffff; padding: 15px 25px; border-radius: 14px; 
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05); border: 1px solid #d2f3ee;
            border-left: 5px solid #d2f3ee; font-family: 'Inter', sans-serif; margin-bottom: 35px; margin-left: 10px; margin-right: 10px;">
    <div style="color: #7c2d12; font-weight: 500;">
        🌬️ Vent : <span style="font-weight: 700; color: #451a03;">{vent_cardinal} ({int(wind_dir)}°)</span> | 
        🚀 Vitesse : <span style="font-weight: 700; color: #451a03;">{int(wind_speed)} km/h</span>
    </div>
</div>
""")

# 3. Base de données
donnees_plages = [
    {"Nom": "Plage de la Passagère", "Secteur": "Saint-Malo / St-Servan", "Orientation": "Sud-Ouest", "Min": 315, "Max": 135, "Ville": "Saint-Malo"},
    {"Nom": "Plage des Sablons", "Secteur": "Saint-Malo / St-Servan", "Orientation": "Nord-Ouest", "Min": 45, "Max": 225, "Ville": "Saint-Malo"},
    {"Nom": "Plage de Bon-Secours", "Secteur": "Saint-Malo (Remparts)", "Orientation": "Ouest", "Min": 360, "Max": 180, "Ville": "Saint-Malo"},
    {"Nom": "Plage du Sillon", "Secteur": "Saint-Malo (Paramé)", "Orientation": "Nord-Ouest", "Min": 45, "Max": 225, "Ville": "Saint-Malo"},
    {"Nom": "Plage des Chevrets", "Secteur": "Rothéneuf / St-Coulomb", "Orientation": "Nord-Nord-Ouest", "Min": 22, "Max": 202, "Ville": "Saint-Coulomb"},
    {"Nom": "Plage de Port Mer", "Secteur": "Cancale", "Orientation": "Est", "Min": 180, "Max": 360, "Ville": "Cancale"}
]
df = pd.DataFrame(donnees_plages)

def est_abritee(row, angle, vitesse):
    if vitesse < 10.0: return True
    mn, mx = row["Min"], row["Max"]
    return (mn <= angle <= mx) if (mn <= mx) else (angle >= mn or angle <= mx)

df["Protégée"] = df.apply(lambda row: est_abritee(row, wind_dir, wind_speed), axis=1)

# 4. Affichage en Liste Verticale
st.markdown("<h3 style='color: #ffffff;'>Plages</h3>", unsafe_allow_html=True)

for _, p in df.iterrows():
    etat = "✔ ABRITÉE" if p['Protégée'] else "❌ EXPOSÉE"
    couleur_badge = "#e6f4ea" if p['Protégée'] else "#fce8e6"
    texte_badge = "#137333" if p['Protégée'] else "#c5221f"
    lien_maps = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(f'{p['Nom']} {p['Ville']}')}"
    
    st.html(f"""
    <div style="background-color: #ffffff; padding: 15px; border-radius: 12px; margin-bottom: 10px;
                border: 1px solid #d2f3ee; display: flex; justify-content: space-between; align-items: center;">
        <div>
            <a href="{lien_maps}" target="_blank" style="text-decoration: none; color: #451a03; font-weight: 700; font-size: 16px;">{p['Nom']}</a>
            <div style="font-size: 12px; color: #7c2d12;">{p['Secteur']} • Face : {p['Orientation']}</div>
        </div>
        <div style="background-color: {couleur_badge}; color: {texte_badge}; padding: 4px 10px; border-radius: 15px; font-weight: 700; font-size: 11px;">
            {etat}
        </div>
    </div>
    """)
