# Dans l'onglet de ton choix ou dans une section dédiée :
st.markdown("<div class='title-box-section' style='margin: 20px auto;'><h3>Webcam - Le Sillon en direct</h3></div>", unsafe_allow_html=True)

# Exemple d'intégration d'une balise iframe ou d'un flux vidéo
st.markdown("""
<div class='rect-style' style='padding:15px; max-width:700px; margin:0 auto; text-align:center;'>
    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
        <!-- Remplace l'URL ci-dessous par le lien direct de la webcam ou son iframe -->
        <iframe src="URL_DE_LA_WEBCAM_DES_THERMES" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border:0;" allowfullscreen></iframe>
    </div>
    <p style="margin-top:10px; font-size:0.85em; color:#444;">Vue en direct sur la digue et la plage du Sillon depuis les Thermes Marins.</p>
</div>
""", unsafe_allow_html=True)
