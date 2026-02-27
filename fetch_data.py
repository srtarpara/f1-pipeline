import requests
import json

url = "https://api.openf1.org/v1/drivers?session_key=latest"

response = requests.get(url)
data = response.json()

for driver in data:
    print(f"{driver['full_name']} - {driver['team_name']}")