import streamlit as st
import pandas as pd
import requests
import urllib.parse

# 1. Configuration de la page
st.set_page_config(
    page_title="Girouette - Abri Plages", 
    page_icon="🏖️",
    layout="centered"
)

st.title("🏖️ Girouette")
st.subheader("Trouvez la plage idéale à l'abri du vent")

# 2. Récupération de la météo en direct (version ultra-compatible)
@st.cache_data(ttl=900)
def get_current_wind():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=48.6493&longitude=-2.0089&current=wind_speed_10m,wind_direction_10m&timezone=Europe%2FParis"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return float(data['current']['wind_direction_10m']), float(data['current']['wind_speed_10m']), True
    except Exception:
        pass
    return 0.0, 15.0, False # Valeurs de secours réalistes si l'API ne répond pas temporairement

wind_dir, wind_speed, meteo_dispo = get_current_wind()

# Options et Mode Manuel
with st.expander("⚙️ Options et Mode Manuel"):
    auto_mode = st.checkbox("Météo en direct", value=meteo_dispo, disabled=not meteo_dispo)
    if not auto_mode:
        wind_dir = st.slider("Direction (degrés)", 0, 360, int(wind_dir))
        wind_speed = st.slider("Vitesse (km/h)", 0, 80, int(wind_speed))

# Calcul de la direction cardinale
directions_texte = ["Nord ⬇️", "Nord-Est ↙️", "Est ⬅️", "Sud-Est ↖️", "Sud ⬆️", "Sud-Ouest ↗️", "Ouest ➡️", "Nord-Ouest ↘️", "Nord ⬇️"]
index_dir = int(round(((wind_dir % 360) / 45)))
vent_cardinal = directions_texte[index_dir]

# Affichage des statistiques du vent
col_m1, col_m2 = st.columns(2)
with col_m1:
    st.metric(label="💨 Direction du vent", value=vent_cardinal, delta=f"{int(wind_dir)}°")
with col_m2:
    st.metric(label="🚀 Vitesse du vent", value=f"{int(wind_speed)} km/h")

st.markdown("---")

# 3. Données des plages
donnees_plages = [
    {"Nom": "Plage de la Passagère", "Secteur": "Saint-Malo / St-Servan", "Orientation": "Sud-Ouest", "Min": 315, "Max": 135, "Ville": "Saint-Malo"},
    {"Nom": "Plage des Fours à Chaux", "Secteur": "Saint-Malo / St-Servan", "Orientation": "Sud-Ouest", "Min": 315, "Max": 135, "Ville": "Saint-Malo"},
    {"Nom": "Plage Saint-Père (Solidor)", "Secteur": "Saint-Malo / St-Servan", "Orientation": "Sud-Ouest", "Min": 315, "Max": 135, "Ville": "Saint-Malo"},
    {"Nom": "Plage des Sablons", "Secteur": "Saint-Malo / St-Servan", "Orientation": "Nord-Ouest", "Min": 45, "Max": 225, "Ville": "Saint-Malo"},
    {"Nom": "Plage de Bon-Secours", "Secteur": "Saint-Malo (Remparts)", "Orientation": "Ouest", "Min": 360, "Max": 180, "Ville": "Saint-Malo"},
    {"Nom": "Plage de l'Éventail", "Secteur": "Saint-Malo (Remparts)", "Orientation": "Ouest", "Min": 360, "Max": 180, "Ville": "Saint-Malo"},
    {"Nom": "Plage du Sillon", "Secteur": "Saint-Malo (Paramé)", "Orientation": "Nord-Ouest", "Min": 45, "Max": 225, "Ville": "Saint-Malo"},
    {"Nom": "Plage du Val", "Secteur": "Rothéneuf", "Orientation": "Nord-Ouest", "Min": 45, "Max": 225, "Ville": "Rothéneuf"},
    {"Nom": "Plage des Chevrets", "Secteur": "Rothéneuf / St-Coulomb", "Orientation": "Nord-Nord-Ouest", "Min": 22, "Max": 202, "Ville": "Saint-Coulomb"},
    {"Nom": "Plage de la Touesse", "Secteur": "Saint-Coulomb", "Orientation": "Nord", "Min": 90, "Max": 270, "Ville": "Saint-Coulomb"},
    {"Nom": "Anse du Guesclin", "Secteur": "Saint-Coulomb", "Orientation": "Nord-Ouest", "Min": 45, "Max": 225, "Ville": "Saint-Coulomb"},
    {"Nom": "Plage du Verger", "Secteur": "Saint-Coulomb", "Orientation": "Nord-Ouest", "Min": 45, "Max": 225, "Ville": "Saint-Coulomb"},
    {"Nom": "Plage de Port Mer", "Secteur": "Cancale", "Orientation": "Est", "Min": 180, "Max": 360, "Ville": "Cancale"}
]
df = pd.DataFrame(donnees_plages)

def est_abritee(row, angle):
    mn, mx = row['Min'], row['Max']
    return (mn <= angle <= mx) if (mn <= mx) else (angle >= mn or angle <= mx)

df['Protégée'] = df.apply(lambda row: est_abritee(row, wind_dir), axis=1)

# 4. Affichage des fiches individuelles
st.write("### 🟢 Plages à l'abri conseillées")
abritees = df[df['Protégée'] == True]

if not abritees.empty:
    for _, p in abritees.iterrows():
        texte_recherche = f"{p['Nom']} {p['Ville']}"
        lien_maps = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(texte_recherche)}"
        
        with st.container(border=True):
            col_plage, col_badge = st.columns([3, 1])
            with col_plage:
                st.markdown(f"📌 **[{p['Nom']}]({lien_maps})**")
                st.caption(f"🌊 {p['Secteur']} • Face mer : {p['Orientation']}")
            with col_badge:
                st.write("")
                st.markdown('<span style="background-color:#e6f4ea; color:#137333; padding:6px 12px; border-radius:20px; font-weight:bold; font-size:12px; display:inline-block; text-align:center; width:100px;">✔ ABRITÉE</span>', unsafe_allow_html=True)
else:
    st.info("Aucun abri idéal trouvé pour le moment.")

st.write("")

with st.expander("🔴 Voir les plages exposées (Vent de face)"):
    exposees = df[df['Protégée'] == False]
    for _, p in exposees.iterrows():
        texte_recherche = f"{p['Nom']} {p['Ville']}"
        lien_maps = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(texte_recherche)}"
        
        with st.container(border=True):
            col_plage, col_badge = st.columns([3, 1])
            with col_plage:
                st.markdown(f"💨 **[{p['Nom']}]({lien_maps})**")
                st.caption(f"🌊 {p['Secteur']} • Face mer : {p['Orientation']}")
            with col_badge:
                st.write("")
                st.markdown('<span style="background-color:#fce8e6; color:#c5221f; padding:6px 12px; border-radius:20px; font-weight:bold; font-size:12px; display:inline-block; text-align:center; width:100px;">❌ EXPOSÉE</span>', unsafe_allow_html=True)
