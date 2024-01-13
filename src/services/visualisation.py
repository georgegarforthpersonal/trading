import plotly.graph_objects as go
from models import Candle


def plot_candlestick_chart(candles: list[Candle]) -> go.Figure():
    fig = go.Figure(data=[go.Candlestick(x=[candle.time for candle in candles],
                                         open=[float(candle.mid.o) for candle in candles],
                                         high=[float(candle.mid.h) for candle in candles],
                                         low=[float(candle.mid.l) for candle in candles],
                                         close=[float(candle.mid.c) for candle in candles])])

    fig.update_layout(xaxis_rangeslider_visible=False, title="Candlestick Chart",
                      xaxis_title="Time", yaxis_title="Price")

    return fig
