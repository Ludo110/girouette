import streamlit as st

st.set_page_config(
    page_title="Maquette Girouette - Style Galerie", 
    page_icon="🏖️",
    layout="wide" # "wide" permet d'utiliser toute la largeur de l'écran pour faire des lignes de fiches
)

# Style de fond (gris très clair pour détacher les cartes blanches)
st.html("""
<style>
    .stApp {
        background-color: #f8fafc !important;
    }
</style>
""")

# 1. EN-TÊTE ÉPURÉ SANS BORDS
st.html("""
<div style="font-family: 'Inter', sans-serif; margin-bottom: 30px; padding-left: 10px;">
    <h1 style="color: #0f172a; font-size: 36px; font-weight: 800; margin-bottom: 5px;">🏖️ Girouette</h1>
    <p style="color: #64748b; font-size: 16px; margin: 0;">Trouvez la plage idéale à l'abri du vent</p>
</div>
""")

# 2. BANDEAU MÉTÉO COMPACT
st.html("""
<div style="display: flex; justify-content: flex-start; gap: 40px; align-items: center; 
            background-color: #ffffff; padding: 15px 25px; border-radius: 14px; 
            box-shadow: 0 1px 3px rgba(0,0,0,0.05); border: 1px solid #e2e8f0;
            font-family: 'Inter', sans-serif; margin-bottom: 35px; margin-left: 10px; margin-right: 10px;">
    <div style="font-size: 16px; color: #334155; font-weight: 500;">
        🌬️ Vent actuel : <span style="font-weight: 700; color: #0f172a;">Nord ⬇️ (22°)</span>
    </div>
    <div style="border-left: 1px solid #e2e8f0; height: 25px;"></div>
    <div style="font-size: 16px; color: #334155; font-weight: 500;">
        🚀 Vitesse : <span style="font-weight: 700; color: #0f172a;">14 km/h</span>
    </div>
</div>
""")

with st.expander("⚙️ Options et Mode Manuel"):
    st.checkbox("Utiliser la météo en direct", value=True)

st.markdown("### 🟢 Plages à l'abri conseillées")

# 3. LA GRILLE HORIZONTALE (Style image d95a5d)
# On crée 3 colonnes pour aligner les plages côte à côte sur l'écran
col1, col2, col3 = st.columns(3)

with col1:
    # Carte Plage 1
    st.html("""
    <div style="background-color: #ffffff; border-radius: 16px; overflow: hidden;
                box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03); 
                border: 1px solid #e2e8f0; font-family: 'Inter', sans-serif; min-height: 180px;
                display: flex; flex-direction: column; justify-content: space-between; padding: 20px;">
        <div>
            <a href="#" style="text-decoration: none; color: #1e3a8a; font-weight: 800; font-size: 18px; display: block; margin-bottom: 8px;">
                📌 Plage de la Passagère
            </a>
            <span style="color: #64748b; font-size: 13px; display: block; line-height: 1.4;">
                🌊 Saint-Malo / St-Servan<br>🧭 Face mer : Sud-Ouest
            </span>
        </div>
        <div style="margin-top: 15px; background-color: #e6f4ea; color: #137333; padding: 6px 0; border-radius: 20px; font-weight: 700; font-size: 12px; letter-spacing: 0.5px; text-align: center; width: 100px;">
            ✔ ABRITÉE
        </div>
    </div>
    """)

with col2:
    # Carte Plage 2
    st.html("""
    <div style="background-color: #ffffff; border-radius: 16px; overflow: hidden;
                box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03); 
                border: 1px solid #e2e8f0; font-family: 'Inter', sans-serif; min-height: 180px;
                display: flex; flex-direction: column; justify-content: space-between; padding: 20px;">
        <div>
            <a href="#" style="text-decoration: none; color: #1e3a8a; font-weight: 800; font-size: 18px; display: block; margin-bottom: 8px;">
                📌 Plage de Bon-Secours
            </a>
            <span style="color: #64748b; font-size: 13px; display: block; line-height: 1.4;">
                🌊 Saint-Malo (Remparts)<br>🧭 Face mer : Ouest
            </span>
        </div>
        <div style="margin-top: 15px; background-color: #e6f4ea; color: #137333; padding: 6px 0; border-radius: 20px; font-weight: 700; font-size: 12px; letter-spacing: 0.5px; text-align: center; width: 100px;">
            ✔ ABRITÉE
        </div>
    </div>
    """)

with col3:
    # Carte Plage 3
    st.html("""
    <div style="background-color: #ffffff; border-radius: 16px; overflow: hidden;
                box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03); 
                border: 1px solid #e2e8f0; font-family: 'Inter', sans-serif; min-height: 180px;
                display: flex; flex-direction: column; justify-content: space-between; padding: 20px;">
        <div>
            <a href="#" style="text-decoration: none; color: #1e3a8a; font-weight: 800; font-size: 18px; display: block; margin-bottom: 8px;">
                📌 Plage des Fours à Chaux
            </a>
            <span style="color: #64748b; font-size: 13px; display: block; line-height: 1.4;">
                🌊 Saint-Malo / St-Servan<br>🧭 Face mer : Sud-Ouest
            </span>
        </div>
        <div style="margin-top: 15px; background-color: #e6f4ea; color: #137333; padding: 6px 0; border-radius: 20px; font-weight: 700; font-size: 12px; letter-spacing: 0.5px; text-align: center; width: 100px;">
            ✔ ABRITÉE
        </div>
    </div>
    """)

st.html("<br><br>")

with st.expander("🔴 Voir les plages exposées (Vent
