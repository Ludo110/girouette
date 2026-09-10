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
        
        # Extraction de TOUTES les heures au format HHhMM ou HH:MM de la page dans l'ordre
        raw_heures = re.findall(r'(\d{2}[h:]\d{2})', html)
        toutes_heures = [h.replace("h", ":") for h in raw_heures]
        
        # On nettoie pour éliminer les doublons successifs rapprochés (dus aux affichages mobiles/desktop du site)
        heures_uniques = []
        for h in toutes_heures:
            if not heures_uniques or h != heures_uniques[-1]:
                heures_uniques.append(h)
        
        # Chaque jour possède exactement 4 marées (2 BM, 2 PM). 
        # Bloc 0 = Aujourd'hui, Bloc 1 = Demain, Bloc 2 = Après-demain...
        start_idx = delta_jours * 4
        
        if start_idx + 4 <= len(heures_uniques):
            heures_jour = heures_uniques[start_idx : start_idx + 4]
        else:
            # Fallbacks de secours si la liste est trop courte
            heures_jour = ["01:03", "06:37", "13:26", "18:56"] if delta_jours == 0 else ["01:52", "07:22", "14:10", "19:39"]

        bms = [heures_jour[0], heures_jour[2]]
        pms = [heures_jour[1], heures_jour[3]]

        next_pm = next((h for h in pms if h >= heure_curr_str), pms[0] if pms else "--:--")
        next_bm = next((h for h in bms if h >= heure_curr_str), bms[0] if bms else "--:--")
        
        return next_pm, next_bm
    except Exception:
        return "18:56", "13:26"
