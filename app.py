import streamlit as st
import requests
import re

st.set_page_config(page_title="Test Marée Aujourd'hui", layout="centered")

st.title("🌊 Test Marée - Aujourd'hui uniquement")

@st.cache_data(ttl=3600)
def recuperer_maree_du_jour():
    try:
        url = "https://horaire-maree.fr/maree/SAINT-MALO/"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        resp = requests.get(url, headers=headers, timeout=5)
        html = resp.text

        # On cherche spécifiquement le premier bloc du haut de la page (les marées du jour)
        # Sur ce site, le premier tableau ou bloc contient les 4 horaires d'aujourd'hui
        match_bloc = re.search(r'<table[^>]*>.*?</table>', html, re.DOTALL)
        if match_bloc:
            zone_haut = match_bloc.group(0)
        else:
            zone_haut = html[:3000] # Fallback sur le début de la page

        raw_heures = re.findall(r'(\d{2}[h:]\d{2})', zone_haut)
        heures = [h.replace("h", ":") for h in raw_heures]

        # On prend les 4 premières heures uniques trouvées dans ce premier bloc
        uniques = []
        for h in heures:
            if h not in uniques:
                uniques.append(h)

        return uniques[:4]
    except Exception as e:
        return [str(e)]

horaires_du_jour = recuperer_maree_du_jour()

st.subheader("Horaires bruts extraits pour aujourd'hui :")
st.write(horaires_du_jour)

if len(horaires_du_jour) >= 4:
    st.success(f"""
    - **Basse mer 1** : {horaires_du_jour[0]}
    - **Pleine mer 1** : {horaires_du_jour[1]}
    - **Basse mer 2** : {horaires_du_jour[2]}
    - **Pleine mer 2** : {horaires_du_jour[3]}
    """)
