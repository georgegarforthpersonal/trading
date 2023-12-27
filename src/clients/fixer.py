from datetime import datetime, timedelta

import requests

FIXER_BASE_URL = "http://data.fixer.io/api"
FIXER_API_KEY = "372a3c2d1fde660e7c14be8e435e6042"


def get_latest():
    url = f"{FIXER_BASE_URL}/latest?access_key={FIXER_API_KEY}"
    response = requests.request("GET", url)
    return response.text


def get_historical(date: str, base: str) -> dict:
    """date provided in the form 2013-12-24"""
    """base currency restricted to EUR for free plan"""
    url = f"{FIXER_BASE_URL}/{date}?access_key={FIXER_API_KEY}&base={base}"
    response = requests.request("GET", url)
    return response.json()


def get_timeseries(start_date: str, end_date: str) -> dict:
    """date provided in the form 2013-12-24"""
    url = f"{FIXER_BASE_URL}/timeseries?access_key={FIXER_API_KEY}&{start_date}&{end_date}"
    response = requests.request("GET", url)
    return response.json()


# if __name__ == "__main__":
#
#     start_date = datetime(2022, 1, 1)
#     for i in range(3):
#         s = start_date.strftime("%Y-%m-%d")
#         print(get_historical(s, "EUR"))
#         start_date += timedelta(days=1)
#
# print('y')


