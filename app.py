import pandas as pd
import requests
import streamlit as st
import urllib.parse

# 1. Configuration de la page en mode LARGE pour la grille
st.set_page_config(page_title="Girouette - Abri Plages", page_icon="🏖️", layout="wide")

# Style de fond : Le bleu-vert canard exact (#568E94) + Couleur crème pour le texte du volet
st.html("""
<style>
    .stApp {
        background-color: #568E94 !important;
    }
    /* Cible le texte du volet pour le mettre en crème */
    .stExpander summary {
        color: #ffedd5 !important;
    }
</style>
""")

# En-tête (Texte blanc et crème pour ressortir sur le fond color
