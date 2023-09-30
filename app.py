from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

import sys
import os
root_path = os.path.dirname(os.getcwd()) 
sys.path.append(root_path)

import alpaca_trade_api as tradeapi
import config as cf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src import alpaca
from src import plotting
import plotly.io as pio

# Instantiate REST API Connection
api = tradeapi.REST(key_id=cf.APCA_API_KEY, secret_key=cf.APCA_SECRET_KEY, 
                    base_url=cf.APCA_MARKET_BASE_URL, api_version='v2')

APPLE_DATA = api.get_bars('AAPL', start = "2022-09-29", end = "2023-09-29", timeframe="1Day", limit=100).df

APPLE_DATA['20_SMA'] = APPLE_DATA['close'].rolling(window = 20, min_periods=1).mean()
APPLE_DATA['10_SMA'] = APPLE_DATA['close'].rolling(window = 10, min_periods=1).mean()
APPLE_DATA['buy'] =((APPLE_DATA['10_SMA'] > APPLE_DATA['20_SMA']) & (APPLE_DATA['10_SMA'].shift(-1) < APPLE_DATA['20_SMA'].shift(-1)))
APPLE_DATA['sell'] =((APPLE_DATA['10_SMA'] < APPLE_DATA['20_SMA']) & (APPLE_DATA['10_SMA'].shift(-1) > APPLE_DATA['20_SMA'].shift(-1)))
buy_list = APPLE_DATA[APPLE_DATA['buy']].index.tolist()
sell_list = APPLE_DATA[APPLE_DATA['sell']].index.tolist()

fig = go.Figure()
for tag in ['close', '10_SMA', '20_SMA']:
    fig.add_trace(go.Scatter(
        x = APPLE_DATA.index,
        y = APPLE_DATA[tag],
        name = tag
))

for buy in buy_list:
    fig.add_vrect(x0=buy-pd.Timedelta(hours = 6), x1=buy+pd.Timedelta(hours = 6),line_width=0, fillcolor="green", opacity=0.5)
for sell in sell_list:
    fig.add_vrect(x0=sell-pd.Timedelta(hours = 6), x1=sell+pd.Timedelta(hours = 6),line_width=0, fillcolor="red", opacity=0.5)


app = Dash(__name__)

# App layout
app.layout = html.Div([
    dcc.Graph(figure=fig)
])


if __name__ == '__main__':
    app.run(debug=True)
