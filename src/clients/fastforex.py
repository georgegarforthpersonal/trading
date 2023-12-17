import requests

FF_BASE_URL = "https://api.fastforex.io"
FF_API_KEY = "60efacb25b-f5cabde71b-s2mytj"


def get_timeseries(cur_from: str, cur_to: str, date_start: str, date_end: str):

    url = f"{FF_BASE_URL}/time-series?from={cur_from}&to={cur_to}" \
          f"&start={date_start}&end={date_end}&api_key={FF_API_KEY}"
    print(url)
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)

    return response.json()
