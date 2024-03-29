import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from models import Candle
from datetime import datetime, date


def plot_candlestick_chart(candles: list[Candle]) -> go.Figure():
    fig = go.Figure(data=[go.Candlestick(x=[candle.time for candle in candles],
                                         open=[float(candle.mid.o) for candle in candles],
                                         high=[float(candle.mid.h) for candle in candles],
                                         low=[float(candle.mid.l) for candle in candles],
                                         close=[float(candle.mid.c) for candle in candles])])

    fig.update_layout(xaxis_rangeslider_visible=False, title="Candlestick Chart",
                      xaxis_title="Time", yaxis_title="Price")

    return fig


def plot_profits(data: list[list[datetime.date, str, float]]):
    """Plot profits and losses for each currency pair over time."""
    df = pd.DataFrame(data, columns=['date', 'currency_pair', 'profit'])
    df['total_profit'] = df['profit'].cumsum()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    currency_pairs = list(set(df['currency_pair'].unique()))
    for currency_pair in currency_pairs:
        df_ = df[df['currency_pair'] == currency_pair]
        fig.add_trace(go.Bar(x=df_['date'], y=df_['profit'], name=currency_pair), secondary_y=False)

    df['total_profit'] = df['profit'].cumsum()
    df_total_profit = df.drop_duplicates(subset='date', keep='last')[['date', 'total_profit']]
    fig.add_trace(go.Scatter(
        x=df_total_profit['date'],
        y=df_total_profit['total_profit'], name='Total profit', line_color='black'), secondary_y=True
    )

    fig.update_layout(
        barmode='relative',
        yaxis_title='Trade close profit (£)',
        yaxis2_title='Profit to date (£)',
    )
    return fig
