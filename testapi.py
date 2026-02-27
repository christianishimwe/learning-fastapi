import requests

BASE_URL = "https://learning-fastapi-258839900414.europe-west1.run.app"

# Test the root endpoint
r = requests.get(f"{BASE_URL}/")
print(f"Root endpoint: {r.json()}")

r = requests.get(f"{BASE_URL}/user")
print(r.json())