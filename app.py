# -----------------------------------------------------------------------------
# ONGLET 4 : PÊCHE & ACTIVITÉ SOLUNAIRE
# -----------------------------------------------------------------------------
elif st.session_state["onglet"] == "peche":
    st.markdown(f"""
    <div class='rect-style' style='padding:12px; text-align:center; max-width:680px; margin:15px auto 25px auto; color:#222;'>
        <b>Activité Pêche & Solunaire {label_jour}</b><br>
        🌊 <b>Mer :</b> PM {haute_mer} — BM {basse_mer}<br>
        🔒 <b>Rance (Amont) :</b> Hauts {rance_info['hauts']} — Bas {rance_info['bas']}
    </div>
    """, unsafe_allow_html=True)

    components.html("""
    <div class="rect-style" style="background-color: rgba(240, 237, 230, 0.85); border-radius: 15px; padding: 25px; max-width: 650px; margin: 0 auto; color: #222; text-align: center; font-family: sans-serif; box-shadow: 0 8px 16px rgba(0,0,0,0.15);">
        <h3 style="color:#436e64; margin-top:0;">Activité modérée</h3>
        <p style="margin: 5px 0 15px 0; font-size: 0.95em; color:#555;">🟣 Premier croissant · Coef. 74</p>
        
        <div style="background: rgba(255,255,255,0.7); border-radius: 12px; padding: 10px; margin-bottom: 20px; font-weight: bold; color:#333;">
            Prochaine période dans 3 h 26
        </div>

        <div style="display: flex; flex-direction: column; gap: 8px;">
            <div style="background: rgba(255,255,255,0.5); padding: 12px 15px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
                <b style="color:#436e64;">Période majeure</b>
                <span>04h47 → 06h47 <i style="font-size:0.85em; color:#555;">Montante</i></span>
            </div>
            <div style="background: rgba(255,255,255,0.5); padding: 12px 15px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
                <b style="color:#557a70;">Période mineure</b>
                <span>13h39 → 14h39 <i style="font-size:0.85em; color:#555;">Descendante</i></span>
            </div>
            <div style="background: rgba(255,255,255,0.5); padding: 12px 15px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
                <b style="color:#436e64;">Période majeure</b>
                <span>17h08 → 19h08 <i style="font-size:0.85em; color:#555;">Montante</i></span>
            </div>
            <div style="background: rgba(255,255,255,0.5); padding: 12px 15px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
                <b style="color:#557a70;">Période mineure</b>
                <span>21h36 → 22h36 <i style="font-size:0.85em; color:#555;">Montante</i></span>
            </div>
        </div>

        <p style="margin-top:20px; font-size:0.8em; font-style:italic; color:#666;">
            Périodes solunaires indicatives (activité théorique des poissons). Marée et coefficient restent calculés.
        </p>
    </div>
    """, height=410, scrolling=False)
