# [ ... Reste du code inchangé ... ]

# Affichage protégées
st.markdown("<h3 style='color: #ffffff; text-align: center;'>🟢 À l'abri</h3>", unsafe_allow_html=True)
cols = st.columns(max(len(abritees), 1))
for i, p in enumerate(abritees):
    with cols[i]:
        lien_maps = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(f'{p['Nom']} {p['Ville']}')}"
        
        # Logique corrigée : Si le secteur est vide ou identique à la ville, on n'affiche que la ville
        info_secteur = f"<br>{p['Secteur']}" if p['Secteur'] and p['Secteur'] != p['Ville'] else ""
        
        st.html(f"""
        <a href="{lien_maps}" target="_blank" style="text-decoration: none;">
            <div class="plage-card">
                <h3 style="color: #333; margin: 0;">{p['Nom']}</h3>
                <p style="color: #555; font-size: 0.9em;">{p['Ville']}{info_secteur}</p>
                <div style="color: #2d5a27; font-weight: bold;">✔ IDÉALE</div>
            </div>
        </a>
        """)

# [ ... Reste du code inchangé ... ]
