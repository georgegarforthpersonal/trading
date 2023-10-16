import requests

FIXER_BASE_URL = "http://data.fixer.io/api"
FIXER_API_KEY = "372a3c2d1fde660e7c14be8e435e6042"

def get_latest():
    url = f"{FIXER_BASE_URL}/latest?access_key={FIXER_API_KEY}"
    response = requests.request("GET", url)
    return response.text


def get_historical(date: str) -> dict:
    """date provided in the form 2013-12-24"""
    url = f"{FIXER_BASE_URL}/{date}?access_key={FIXER_API_KEY}"
    response = requests.request("GET", url)
    return response.json()


def get_timeseries(start_date: str, end_date: str) -> dict:
    """date provided in the form 2013-12-24"""
    url = f"{FIXER_BASE_URL}/timeseries?access_key={FIXER_API_KEY}&{start_date}&{end_date}"
    response = requests.request("GET", url)
    return response.json()

if __name__ == "__main__":

    print(get_latest())



