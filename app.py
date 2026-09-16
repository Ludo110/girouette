# Test d'encart Rance Amont vs Mer
st.markdown("""
<div class='rect-style' style='padding:20px; max-width:600px; margin:15px auto; color:#222;'>
    <h3 style='text-align:center; color:#436e64; margin-top:0;'>🌊 Mer (Saint-Malo) vs Rance (Amont Barrage)</h3>
    <div style='display:flex; justify-content:space-around; flex-wrap:wrap; gap:15px; text-align:center;'>
        <div style='flex: 1; min-width: 220px; background: rgba(255,255,255,0.5); padding: 10px; border-radius: 10px;'>
            <b>🌊 Mer Ouverte</b><br>
            Pleine mer : <b>{haute_mer}</b><br>
            Basse mer : <b>{basse_mer}</b>
        </div>
        <div style='flex: 1; min-width: 220px; background: rgba(255,255,255,0.5); padding: 10px; border-radius: 10px;'>
            <b>🔒 Rance (Amont Barrage)</b><br>
            Retenue régulée (faible marnage)<br>
            <i>Écluse :</i> selon paliers de marée (> +4m)
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
