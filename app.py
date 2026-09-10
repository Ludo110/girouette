@st.cache_data(ttl=3600)
def _fetch_horaire_maree_site():
    try:
        url = "https://horaire-maree.fr/maree/SAINT-MALO/"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        resp = requests.get(url, headers=headers, timeout=5)
        return resp.text
    except Exception:
        return ""

def récupérer_marées_réelles(dt_cible):
    try:
        html = _fetch_horaire_maree_site()
        heure_curr_str = dt_cible.strftime("%H:%M")
        delta_jours = (dt_cible - now_france.date()).days
        
        # On extrait toutes les lignes de tableaux (<tr>) du site
        lignes_tr = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL)
        
        jours_marées = []
        for ligne in lignes_tr:
            # On cherche les heures au format HHhMM dans chaque ligne de tableau
            h_trouvees = [h.replace("h", ":") for h in re.findall(r'(\d{2}h\d{2})', ligne)]
            # Une ligne de marée complète contient exactement 4 horaires (2 basses mers, 2 pleines mers)
            if len(h_trouvees) >= 4:
                bloc = h_trouvees[:4]
                if bloc not in jours_marées:
                    jours_marées.append(bloc)
                    
        # jours_marées[0] = Aujourd'hui (le bloc du haut)
        # jours_marées[1] = Demain (première ligne du tableau des 10 jours)
        # jours_marées[2] = Après-demain, etc.
        if 0 <= delta_jours < len(jours_marées):
            heures_jour = jours_marées[delta_jours]
        else:
            # Valeurs de secours si le scraping échoue
            heures_jour = ["01:03", "06:37", "13:26", "18:56"] if delta_jours == 0 else ["01:52", "07:22", "14:10", "19:39"]

        bms = [heures_jour[0], heures_jour[2]]
        pms = [heures_jour[1], heures_jour[3]]

        next_pm = next((h for h in pms if h >= heure_curr_str), pms[0] if pms else "--:--")
        next_bm = next((h for h in bms if h >= heure_curr_str), bms[0] if bms else "--:--")
        
        return next_pm, next_bm
    except Exception:
        return "18:56", "13:26"
