st.markdown("""
<style>
    .stApp { background-color: #5d7689 !important; }
    
    /* Cible le texte de l'expander de façon plus précise pour forcer la couleur */
    div[data-testid="stExpander"] button p { 
        color: #e2dfd7 !important; 
        font-weight: bold !important; 
    }
    
    /* Conteneur parent pour le centrage */
    .centrage-fixe { display: flex; flex-direction: row; justify-content: center; gap: 20px; flex-wrap: wrap; }
    
    /* Style commun pour les rectangles */
    .rect-style { 
        background-color: #e2dfd7; 
        border-radius: 15px; 
        box-shadow: 0 8px 16px rgba(0,0,0,0.2); 
    }
    .plage-card { 
        padding: 20px 10px; text-align: center; width: 200px; height: 250px; 
        display: flex; flex-direction: column; justify-content: flex-start; align-items: center; 
    }
    .card-title { width: 100%; margin: 0 0 10px 0; font-size: 1.2em; text-decoration: underline; }
    .card-text { width: 100%; color: #555; margin: 0 0 10px 0; font-size: 0.9em; }
    a::after { content: none !important; }
</style>
""", unsafe_allow_html=True)
