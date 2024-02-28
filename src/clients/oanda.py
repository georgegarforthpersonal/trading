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

# Initialize the OANDA API
api = API(access_token=OANDA_API_KEY, environment='practice')  # Use 'live' for a live account



def get_latest_candle_data(instrument, granularity, count):
    """
    Get the latest candle data for a specific instrument and granularity.
    count: The number of candlesticks to retrieve (default is 1)
    granularity: The granularity of the candlesticks (default is 'D' for day)
    """

    # Set the parameters for the candle request
    params = {
        'count': count,
        'granularity': granularity,
    }

    request = InstrumentsCandles(instrument=instrument, params=params)
    response = api.request(request)
    data = response['candles']

    return [Candle(**{**item, 'mid': Midpoint(**item['mid'])}) for item in data]


def place_order(data):
    client = API(access_token=OANDA_API_KEY, environment="practice")
    r = orders.OrderCreate(OANDA_ACCOUNT_ID, data=data)
    client.request(r)
    return r.response


def get_trades():
    client = API(access_token=OANDA_API_KEY, environment="practice")
    r = trades.OpenTrades(OANDA_ACCOUNT_ID)
    client.request(r)
    return r.response


def close_trade(trade_id):
    client = API(access_token=OANDA_API_KEY, environment="practice")
    r = trades.TradeClose(accountID=OANDA_ACCOUNT_ID, tradeID=trade_id)
    client.request(r)
    return r.response
