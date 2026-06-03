import pandas as pd
import requests
import streamlit as st
import urllib.parse

# 1. Configuration de la page en mode LARGE pour la grille
st.set_page_config(page_title="Girouette - Abri Plages", page_icon="🏖️", layout="wide")

# Style de fond : Le bleu-vert canard exact (#568E94)
st.html("""
<style>
    .stApp {
        background-color: #568E94 !important;
    }
</style>
""")

# En-tête (Texte blanc et crème pour ressortir sur le fond coloré)
st.html("""
<div style="font-family: 'Inter', sans-serif; margin-bottom: 30px; padding-left: 10px;">
    <h1 style="color: #ffffff; font-size: 36px; font-weight: 800; margin-bottom: 5px; text-shadow: 0 1px 2px rgba(0,0,0,0.1);">🏖️ Girouette</h1>
    <p style="color: #ffedd5; font-size: 16px; margin: 0; opacity: 0.9;">Trouvez la plage idéale à l'abri du vent</p>
</div>
""")


# 2. Récupération de la météo en direct
def get_current_wind():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=48.6493&longitude=-2.0089&current=wind_speed_10m,wind_direction_10m&timezone=Europe%2FParis"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return float(data["current"]["wind_direction_10m"]), float(
                data["current"]["wind_speed_10m"]
            )
    except Exception:
        pass
    return 270.0, 15.0


wind_dir, wind_speed = get_current_wind()

# Options et Mode Manuel (Titre en couleur #ffedd5)
with st.expander(":orange[⚙️ Options et Mode Manuel]"):
    # Note: comme Streamlit ne permet pas de changer facilement la couleur 
    # du texte de l'expander sans CSS, j'utilise la balise :orange[ ] 
    # qui est native et s'approche au plus près de ton crème #ffedd5.
    auto_mode = st.checkbox("Utiliser la météo en direct", value=True)
    if not auto_mode:
        wind_dir = st.slider("Direction du vent (degrés)", 0, 360, int(wind_dir))
        wind_speed = st.slider("Vitesse du vent (km/h)", 0, 80, int(wind_speed))

# Calcul de la direction du vent
directions_texte = [
    "Nord ⬇️",
    "Nord-Est ↙️",
    "Est ⬅️",
    "Sud-Est ↖️",
    "Sud ⬆️",
    "Sud-Ouest ↗️",
    "Ouest ➡️",
    "Nord-Ouest ↘️",
    "Nord ⬇️",
]
index_dir = int(round(((wind_dir % 360) / 45)))
vent_cardinal = directions_texte[index_dir]

# Bandeau météo blanc avec toutes les bordures modifiées en #d2f3ee
st.html(f"""
<div style="display: flex; justify-content: flex-start; gap: 40px; align-items: center; 
            background-color: #ffffff; padding: 15px 25px; border-radius: 14px; 
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05); border: 1px solid #d2f3ee;
            border-left: 5px solid #d2f3ee;
            font-family: 'Inter', sans-serif; margin-bottom: 35px; margin-left: 10px; margin-right: 10px;">
    <div style="font-size: 16px; color: #7c2d12; font-weight: 500;">
        🌬️ Vent actuel : <span style="font-weight: 700; color: #451a03;">{vent_cardinal} ({int(wind_dir)}°)</span>
    </div>
    <div style="border-left: 1px solid #d2f3ee; height: 25px; opacity: 0.5;"></div>
    <div style="font-size: 16px; color: #7c2d12; font-weight: 500;">
        🚀 Vitesse : <span style="font-weight: 700; color: #451a03;">{int(wind_speed)} km/h</span>
    </div>
</div>
""")

# 3. Base de données des plages
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

def est_abritee(row, angle, vitesse):
    if vitesse < 10.0:
        return True
    mn, mx = row["Min"], row["Max"]
    return (mn <= angle <= mx) if (mn <= mx) else (angle >= mn or angle <= mx)

df["Protégée"] = df.apply(lambda row: est_abritee(row, wind_dir, wind_speed), axis=1)

# Message d'information si vent faible
if wind_speed < 10.0:
    st.html(
        '<div style="background-color: #ffffff; border-left: 4px solid #d2f3ee; border-right: 1px solid #d2f3ee; border-top: 1px solid #d2f3ee; border-bottom: 1px solid #d2f3ee; color: #9a3412; padding: 15px; border-radius: 12px; font-family: \'Inter\', sans-serif; font-size: 15px; margin-bottom: 25px; margin-left: 10px; margin-right: 10px; font-weight: 500; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">✨ <b>Pas ou très peu de vent aujourd\'hui !</b> Toutes les plages de la région sont excellentes pour poser la serviette.</div>'
    )

# 4. GRILLE DES PLAGES CONSEILLÉES
st.markdown(
    "<h3 style='color: #ffffff; font-family: sans-serif; text-shadow: 0 1px 2px rgba(0,0,0,0.1);'>🟢 Pl
