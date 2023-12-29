from datetime import datetime
from typing import Optional
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

from logger import setup_logger
from src.clients.database import DatabaseConnection

logger = setup_logger(logger_name=__name__)

app = dash.Dash(__name__)

base_currency_options = ['EUR']
quote_currency_options = ['USD', 'GBP', 'CAD', 'AUD', 'NZD', 'JPY', 'CHF']

app.layout = html.Div([
    html.H1("Currency Data Viewer", style={'textAlign': 'center', 'marginBottom': '20px'}),
    html.Div([
        html.Label("Base Currency:"),
        dcc.Dropdown(id='base-currency',
                     options=[{'label': currency, 'value': currency} for currency in base_currency_options],
                     value='EUR')
    ], style={'marginBottom': '15px'}),
    html.Div([
        html.Label("Quote Currency:"),
        dcc.Dropdown(id='quote-currency',
                     options=[{'label': currency, 'value': currency} for currency in quote_currency_options],
                     value='USD')
    ], style={'marginBottom': '15px'}),
    html.Div([
        html.Label("Select Date Range:"),
        dcc.DatePickerRange(
            id='date-range-picker',
            start_date='2022-01-01',
            end_date='2023-12-31',
            display_format='YYYY-MM-DD'
        )
    ], style={'marginBottom': '15px'}),
    html.Div(id='output-data', style={'marginTop': '20px', 'textAlign': 'center'})  # Display data here
])


@app.callback(
    Output('output-data', 'children'),
    [Input('base-currency', 'value'),
     Input('quote-currency', 'value'),
     Input('date-range-picker', 'start_date'),
     Input('date-range-picker', 'end_date')]
)
def update_data(base_currency, quote_currency, start_date, end_date):
    database_connection = DatabaseConnection()
    timestamp_after = datetime.strptime(start_date, '%Y-%m-%d')
    timestamp_before = datetime.strptime(end_date, '%Y-%m-%d')

    currency_series = database_connection.get_rates_as_series(
        base_currency,
        quote_currency,
        timestamp_after,
        timestamp_before
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=currency_series.index, y=currency_series.values, name=quote_currency))

    graph = dcc.Graph(
        figure=fig,
        style={'height': '400px'}  # Adjust graph height
    )
    return graph


if __name__ == '__main__':
    app.run_server(debug=True)
