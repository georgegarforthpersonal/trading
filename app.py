import sys
from path import Path

root_path = current_script_path = Path(__file__).parent.parent
sys.path.append(root_path)

from datetime import datetime
from src.clients.oanda import get_transactions_since
from logger import setup_logger
from src.services.visualisation import plot_profits
from utils import get_datetime_from_oanda_datetime_str
import streamlit as st


logger = setup_logger(logger_name=__name__)


date_since = datetime(2024, 3, 27)  # Date after which I started automating trades
transaction_reason = 'MARKET_ORDER_TRADE_CLOSE'

all_transactions = get_transactions_since('0')['transactions']
recent_transactions = [t for t in all_transactions if (
    (get_datetime_from_oanda_datetime_str(t['time']) > date_since)
    & (t['reason'] == transaction_reason if 'reason' in t.keys() else False)
)]

data = [[get_datetime_from_oanda_datetime_str(t['time']).date(), t['instrument'], round(float(t['pl']),3)] for t in recent_transactions]
fig = plot_profits(data)

st.set_page_config(layout="wide")
st.title("Currency Trading Profits")
st.plotly_chart(fig, use_container_width=True)


