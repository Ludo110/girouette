import streamlit as st
import requests
import urllib.parse

st.set_page_config(page_title="Girouette Malouine", layout="wide")

st.markdown("""
<style>
    /* Masquer le header, le footer et le menu Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp { background-color: #64978b !important; }
    div[data-testid="stExpander"] button div p { color: #f0ede6 !important; font-weight: bold !important; }
    .centrage-fixe { display: flex; flex-direction: row; justify-content: center; gap: 20px; flex-wrap: wrap; }
    .rect-style { background-color: #f0ede6; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.15); overflow: hidden; }
    .plage-card { padding: 0px 0px 15px 0px; text-align: center; width: 260px; display: flex; flex-direction: column; justify-content: flex-start; align-items: center; }
    .card-img { width: 100%; height: 140px; object-fit: cover; }
    .card-title { width: 100%; margin: 10px 0 5px 0; font-size: 1.1em; text-decoration: underline; }
    .card-text { width: 100%; color: #666; margin: 0 0 10px 0; font-size: 0.85em; }
    a::after { content: none !important; }

    /* Style de l'encadré principal pleine largeur pour le titre */
    .title-box-full {
        background-color: #f0ede6;
        border-radius: 12px;
        padding: 12px 20px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        width: 100%;
        margin-bottom: 15px;
    }
    .title-box-full h1 {
        margin: 0 !important;
        color: #436e64 !important;
        font-size: 1.6em !important;
    }

    /* Style des encadrés pour les sections A l'abri / Exposées */
    .title-box-section {
        background-color: #f0ede6;
        border-radius: 12px;
        padding: 10px 20px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        max-width: 350px;
        margin: 0 auto;
    }
    .title-box-section h3 {
        margin: 0 !important;
        color: #436e64 !important;
        font-size: 1.2em !important;
    }
</style>
""", unsafe_allow_html=True)

plages = [
    {"Nom": "La Passagere", "Ville": "Saint-Malo", "Min": 315, "Max": 135, "Image": "Passagere.jpg"},
    {"Nom": "Fours a Chaux", "Ville": "Saint-Malo", "Min": 315, "Max": 135, "Image": "Foursachaux.jpg"},
    {"Nom": "Saint-Pere", "Ville": "Saint-Malo", "Min": 315, "Max": 135, "Image": "Saint-Pere.jpg"},
    {"Nom": "Les Sablons", "Ville": "Saint-Malo", "Min": 45, "Max": 225, "Image": "Sablons.jpg"},
    {"Nom": "Bon-Secours", "Ville": "Saint-Malo", "Min": 360, "Max": 180, "Image": "Bonsecours.jpg"},
    {"Nom": "L'Eventail", "Ville": "Saint-Malo", "Min": 360, "Max": 180, "Image": "Eventail.jpg"},
    {"Nom": "Le Sillon", "Ville": "Saint-Malo", "Min": 45, "Max": 225, "Image": "Sillon.jpg"},
    {"Nom": "Le Val", "Ville": "Rotheneuf", "Min": 45, "Max": 225, "Image": "Val.jpg"},
    {"Nom": "Les Chevrets", "Ville": "Saint-Coulomb", "Min": 22, "Max": 202, "Image": "Chevrets.jpg"},
    {"Nom": "La Touesse", "Ville": "Saint-Coulomb", "Min": 90, "Max": 270, "Image": "Touesse.jpg"},
    {"Nom": "Le Guesclin", "Ville": "Saint-Coulomb", "Min": 45, "Max": 225, "Image": "Guesclin.jpg"},
    {"Nom": "Le Verger", "Ville": "Saint-Coulomb", "Min": 45, "Max": 225, "Image": "Verger.jpg"},
    {"Nom": "Port Mer", "Ville": "Cancale", "Min": 180, "Max": 360, "Image": "Portmer.jpg"}
]

try:
    r = requests.get("
