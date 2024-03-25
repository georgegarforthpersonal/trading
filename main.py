#!/usr/bin/env python

import sys
from path import Path

root_path = current_script_path = Path(__file__).parent.parent

sys.path.append(root_path)

from logger import setup_logger
from datetime import datetime
from src.clients.oanda import get_latest_candle_data, get_trades, get_open_trades, close_trade, place_order

logger = setup_logger(logger_name=__name__)

CURRENCY_PAIRS = ['GBP_USD', 'USD_JPY', 'GBP_USD', 'USD_CHF', 'AUD_USD', 'USD_CAD', 'NZD_USD']


def get_datetime_from_oanda_datetime_str(datetime_str):
    """Oanda datetime strings are in the format '2022-01-01T00:00:00.000000000Z'"""
    return datetime.strptime(datetime_str.split('.')[0], '%Y-%m-%dT%H:%M:%S')


def main():
    open_trades = get_open_trades()['trades']
    for currency_pair in CURRENCY_PAIRS:
        currency_open_trades = [c for c in open_trades if c['instrument'] == currency_pair]
        latest_complete_candle = get_latest_candle_data(instrument=currency_pair, granularity='D', count=2)[0]
        candle_end = get_datetime_from_oanda_datetime_str(latest_complete_candle.time)
        open = float(latest_complete_candle.mid.o)
        close = float(latest_complete_candle.mid.c)
        price_increase = round(close - open, 3)

        if price_increase > 0:
            logger.info(f"Value of {currency_pair} is {price_increase} greater at {candle_end} than previous day.")
            if len(currency_open_trades) == 0:
                order_data = {
                    "order": {
                        "instrument": currency_pair,
                        "units": "100",
                        "type": "MARKET",
                        "positionFill": "DEFAULT"
                    }
                }
                place_order(order_data)
                logger.info("Order placed.")
            else:
                logger.info("Order already exists.")
        else:
            logger.info(f"Value of {currency_pair} is {-price_increase} lower at {candle_end} than previous day")
            if len(currency_open_trades) == 1:
                close_trade(currency_open_trades[0]['id'])
                logger.info("Trade closed.")
            else:
                logger.info("No trades open.")



if __name__ == '__main__':
    main()