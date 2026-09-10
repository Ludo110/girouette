import streamlit as st
import requests
import re

st.set_page_config(page_title="Test Marée Demain", layout="centered")

st.title("🌊 Test Marée - Demain uniquement")

@st.cache_data(ttl=3600)
def recuperer_maree_demain():
    try:
        url = "https://horaire-maree.fr/maree/SAINT-MALO/"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        resp = requests.get(url, headers=headers, timeout=5)
        html = resp.text

        raw_heures = re.findall(r'(\d{2}[h:]\d{2})', html)
        heures = [h.replace("h", ":") for h in raw_heures]

        uniques = []
        for h in heures:
            if h not in uniques:
                uniques.append(h)

        # Pour demain (delta_jours = 1), on saute les 4 premières heures d'aujourd'hui -> index 4
        start_idx = 4
        if start_idx + 4 <= len(uniques):
            return uniques[start_idx : start_idx + 4]
        else:
            return ["Données insuffisantes"]
    except Exception as e:
        return [str(e)]

horaires_demain = recuperer_maree_demain()

st.subheader("Horaires bruts extraits pour demain :")
st.write(horaires_demain)

if len(horaires_demain) >= 4:
    st.success(f"""
    - **Basse mer 1** : {horaires_demain[0]}
    - **Pleine mer 1** : {horaires_demain[1]}
    - **Basse mer 2** : {horaires_demain[2]}
    - **Pleine mer 2** : {horaires_demain[3]}
    """)
