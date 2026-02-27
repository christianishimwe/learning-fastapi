import requests

BASE_URL = "http://127.0.0.1:8000"

r = requests.post(f"{BASE_URL}/user", json={"id": 5, "name": "Christian"})
print(r.json())
