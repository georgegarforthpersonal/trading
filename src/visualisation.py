from datetime import timedelta, datetime
from typing import Optional

import plotly.graph_objects as go
import pandas as pd


def visualise_currency_series(currency_series: pd.Series) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=currency_series.index, y=currency_series.values))
    return fig


def add_profit_indicators(fig: go.Figure(), profit_list: list[list[datetime, float]]):

    # Restrict shape min and max
    fig_data_list = fig.data
    assert len(fig_data_list) == 1, "Only one trace is supported"
    fig_data = fig_data_list[0]
    y0 = round(fig_data.y.min() - 0.01, 2)
    y1 = round(fig_data.y.max() + 0.01, 2)

    # Add shapes
    shapes = []
    for profit_item in profit_list:
        date = profit_item[0]
        profit = profit_item[1]
        if profit >= 0:
            shapes.append(dict(type="rect",
                               x0=date,
                               y0=y0,
                               x1=date + timedelta(days=1),
                               y1=y1,
                               fillcolor="green",
                               opacity=0.1,
                               line_width=0))
        else:
            shapes.append(dict(type="rect",
                               x0=date,
                               y0=y0,
                               x1=date + timedelta(days=1),
                               y1=y1,
                               fillcolor="red",
                               opacity=0.1,
                               line_width=0))

    fig.update_layout(shapes=shapes)

    return fig


def add_title(fig, investment, profit):
    fig.update_layout(title=f"Investment: {investment} EUR; Profit: {profit} EUR.")
    return fig

