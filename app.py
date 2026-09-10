import requests

url = "https://www.infoclimat.fr/public-api/gfs/json?id=000YV&auth=Tldx1OehbMsR6xzpQDzArHPJkGeBZX9Gb8dF0Qd3pqaUpart2w&format=json"
resp = requests.get(url)
print("Code statut :", resp.status_code)
print("Contenu brut :", resp.text[:500])
