import streamlit as st
import requests

st.set_page_config(page_title="Test Direct Môle", layout="centered")

st.title("Test Relevé Môle des Noires (000YV)")

# URL officielle de l'API Open Data Infoclimat pour les stations StatIC
url = "https://www.infoclimat.fr/public-api/static/json/?id=000YV&auth=QYjEHvFGBaIno2ltwm26cVk8RPx5HwFVnn6did0k3AgIOxWbTfgw&format=json"
