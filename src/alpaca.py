# API Docs: https://docs.alpaca.markets/docs

import requests
import pandas as pd

import config as cf
import src.exceptions as exceptions


def get_account_info():
    
    url = f"{cf.APCA_PAPER_API_BASE_URL}/account"

    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": cf.APCA_API_KEY,
        "APCA-API-SECRET-KEY": cf.APCA_SECRET_KEY
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise exceptions.AlpacaError(response.status_code, response.text)

    return response.json()
    
    
def get_bars(start, end, limit=1000):
    
    """start and end should be in the form "2023-01-01"
    """
    
    url = f"{cf.APCA_MARKET_BASE_URL}/stocks/bars?symbols=AAPL&timeframe=1Min&start={start}&end={end}&limit={limit}&adjustment=raw&feed=sip"
    
    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": cf.APCA_API_KEY,
        "APCA-API-SECRET-KEY": cf.APCA_SECRET_KEY
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise exceptions.AlpacaError(response.status_code, response.text)
    
    df = pd.DataFrame(response.json()['bars']['AAPL'])

    return df
