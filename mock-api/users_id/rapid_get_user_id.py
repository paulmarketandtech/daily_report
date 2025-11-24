import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

url = "https://twitter154.p.rapidapi.com/user/details"

# both parameters are optional
querystring = {"username": "EricJhonsa"}  # ,"user_id":"1096436452576047104"}

headers = {
    "x-rapidapi-key": os.getenv("BIG_BIRD_API_KEY"),
    "x-rapidapi-host": "twitter154.p.rapidapi.com",
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

with open(f"{querystring['username'].lower()}.json", "w") as file:
    json.dump(response.json(), file)
