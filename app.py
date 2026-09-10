import requests

url = "https://www.infoclimat.fr/public-api/static/json/?id=000YV&auth=Tldx1OehbMsR6xzpQDzArHPJkGeBZX9Gb8dF0Qd3pqaUpart2w&format=json"
data = requests.get(url).json()
print(data.get("temperature"))
