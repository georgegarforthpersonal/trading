# OANDA API wrapper docs https://oanda-api-v20.readthedocs.io/en/latest/index.html

import requests
from oandapyV20.contrib.requests import MarketOrderRequest
from oandapyV20.endpoints.orders import OrderCreate

from config import OANDA_API_KEY, OANDA_BASE_URL, OANDA_ACCOUNT_ID
from logger import setup_logger
from oandapyV20 import API
from oandapyV20.exceptions import V20Error
from oandapyV20.endpoints.instruments import InstrumentsCandles
import oandapyV20
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades

from models import Candle, Midpoint

logger = setup_logger(logger_name=__name__)


def get_account_details():
    url = f"{OANDA_BASE_URL}/v3/accounts"
    headers = {
        "Authorization": f"Bearer {OANDA_API_KEY}"
    }
    response = requests.get(url, headers=headers)
    return response.json()


def get_latest_candle_data(instrument='GBP_USD', granularity='D', count=1):
    """
    Get the latest candle data for a specific instrument and granularity.

    Parameters:
    - api_key: Your OANDA API key
    - account_id: Your OANDA account ID
    - instrument: The trading instrument (default is 'GBP_USD')
    - granularity: The granularity of the candlesticks (default is 'D' for day)
    - count: The number of candlesticks to retrieve (default is 1)

    Returns:
    - List of candle data
    """
    # Initialize the OANDA API
    api = API(access_token=OANDA_API_KEY, environment='practice')  # Use 'live' for a live account

    # Set the parameters for the candle request
    params = {
        'count': count,
        'granularity': granularity,
    }

    # Make the request to get candle data
    try:
        request = InstrumentsCandles(instrument=instrument, params=params)
        response = api.request(request)
        data = response['candles']
        return [Candle(**{**item, 'mid': Midpoint(**item['mid'])}) for item in data]

    except V20Error as e:
        print(f"Error retrieving candle data: {e}")
        return None


class OrderSubmitter:
    def __init__(self):
        self.client = oandapyV20.API(access_token=OANDA_API_KEY, environment="practice")
        self.accountID = OANDA_ACCOUNT_ID

    def submit_order(self, data):
        order_request = orders.OrderCreate(accountID=self.accountID, data=data)
        response = self.client.request(order_request)
        return response['orderCreateTransaction']


def get_order_list():
    client = API(access_token=OANDA_API_KEY, environment="practice")
    r = orders.OrderList(OANDA_ACCOUNT_ID)
    client.request(r)
    return r.response