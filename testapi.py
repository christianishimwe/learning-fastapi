import requests

BASE_URL = "https://learning-fastapi-258839900414.europe-west1.run.app"

# Test the root endpoint
r = requests.get(f"{BASE_URL}/")
print(f"Root endpoint: {r.json()}")

#r = requests.post(f"{BASE_URL}/user", json={"id": 5, "name": "Christian"})
r = requests.get(f"{BASE_URL}/items/")
print(r.json())