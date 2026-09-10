import streamlit as st
import requests

url = "https://www.infoclimat.fr/public-api/gfs/json?id=000YV&auth=Tldx1OehbMsR6xzpQDzArHPJkGeBZX9Gb8dF0Qd3pqaUpart2w&format=json"
try:
    resp = requests.get(url)
    st.write("Code statut :", resp.status_code)
    st.write("JSON brut :", resp.json())
except Exception as e:
    st.error(f"Erreur : {e}")
