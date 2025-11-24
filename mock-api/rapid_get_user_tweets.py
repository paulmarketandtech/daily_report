import json
import os
from datetime import date, timedelta

import requests

previous_day = date.today() - timedelta(days=1)

users_name_id_dict = {
    "StockSavvyShay": "1096436452576047104",
    "StockMarketNerd": "1130601604418347008",
    "AIStockSavvy": "72858967",
    "trendforce": "201153042",
    "StockMKTNewz": "1250830691824283648",
    "EricJhonsa": "572077039",
}

url = "https://twitter241.p.rapidapi.com/user-tweets"


for key, value in users_name_id_dict.items():

    querystring = {"user": value, "count": "20"}

    headers = {
        "x-rapidapi-key": os.getenv("BIG_BIRD_API_KEY"),
        "x-rapidapi-host": "twitter241.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)

    with open(
        f"tweets/{str(previous_day).replace('-','')}_{key.lower()}.json", "w"
    ) as file:
        json.dump(response.json(), file)
