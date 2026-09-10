import streamlit as st
import requests

st.set_page_config(page_title="Test Môle des Noires", layout="centered")

st.title("Test direct - Température Môle des Noires (000YV)")

url = "https://www.infoclimat.fr/public-api/static/json/?id=000YV&auth=QYjEHvFGBaIno2ltwm26cVk8RPx5HwFVnn6did0k3AgIOxWbTfgw&format=json"

try:
    resp = requests.get(url, timeout=5)
    st.write("Statut HTTP :", resp.status_code)
    
    data = resp.json()
    st.write("JSON brut reçu :", data)
    
    # Extraction ciblée de la température
    if isinstance(data, dict):
        if "temperature" in data:
            st.metric("Température Môle des Noires", f"{data['temperature']} °C")
        elif "current" in data and isinstance(data["current"], dict) and "temperature" in data["current"]:
            st.metric("Température Môle des Noires", f"{data['current']['temperature']} °C")
        elif "000YV" in data and isinstance(data["000YV"], dict):
            station_info = data["000YV"]
            if "temperature" in station_info:
                st.metric("Température Môle des Noires", f"{station_info['temperature']} °C")
            else:
                st.write("Contenu de la station :", station_info)
        else:
            # Recherche automatique dans les sous-dictionnaires
            found = False
            for k, v in data.items():
                if isinstance(v, dict) and "temperature" in v:
                    st.metric("Température Môle des Noires", f"{v['temperature']} °C")
                    found = True
                    break
            if not found:
                st.warning("La structure JSON ne contient pas de champ 'temperature' direct. Regarde le JSON brut ci-dessus.")
except Exception as e:
    st.error(f"Erreur : {e}")
