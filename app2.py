#!/usr/bin/env python3

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from logger import setup_logger
from src.clients.database import DatabaseConnection
from src.visualisation import visualise_currency_series, add_profit_indicators, add_title
from strategies.previous_days_delta import calculate_statistics, calculate_annual_profit

logger = setup_logger(logger_name=__name__)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])  # Set Bootstrap theme

base_currency_options = ['EUR']
quote_currency_options = ['USD', 'GBP', 'CAD', 'AUD', 'NZD', 'JPY', 'CHF']

strategies = ['Previous Days Delta']

app.layout = dbc.Container([
    dcc.Tabs([
        dcc.Tab(label='Currency Viewer', children=[
            html.H1("Currency Data Viewer", style={'textAlign': 'center', 'marginBottom': '20px'}),
            dbc.Row([
                dbc.Col([
                    html.Label("Base Currency:"),
                    dcc.Dropdown(id='base-currency',
                                 options=[{'label': currency, 'value': currency} for currency in base_currency_options],
                                 value='EUR')
                ], width=6, style={'marginBottom': '15px'}),
                dbc.Col([
                    html.Label("Quote Currency:"),
                    dcc.Dropdown(id='quote-currency',
                                 options=[{'label': currency, 'value': currency} for currency in quote_currency_options],
                                 value='USD')
                ], width=6, style={'marginBottom': '15px'}),
            ]),
            html.Div(id='output-data', style={'marginTop': '20px', 'textAlign': 'center'})  # Display data here
        ]),
        dcc.Tab(label='Strategies', children=[
            html.H1("Strategies", style={'textAlign': 'center', 'marginBottom': '20px'}),
            dbc.Row([
                dbc.Col([
                    html.Label("Base Currency:"),
                    dcc.Dropdown(id='base-currency',
                                 options=[{'label': currency, 'value': currency} for currency in base_currency_options],
                                 value='EUR')
                ], width=6, style={'marginBottom': '15px'}),
                dbc.Col([
                    html.Label("Quote Currency:"),
                    dcc.Dropdown(id='quote-currency',
                                 options=[{'label': currency, 'value': currency} for currency in
                                          quote_currency_options],
                                 value='USD')
                ], width=6, style={'marginBottom': '15px'}),
            ]),
            dbc.Row([
                dbc.Col([
                    html.Label("Strategy:"),
                    dcc.Dropdown(id='strategy',
                                 options=[{'label': strategy, 'value': strategy} for strategy in strategies],
                                 value='Previous Days Delta')
                ], width=6, style={'marginBottom': '15px'}),
            ]),
            html.Div(id='strategy-data', style={'marginTop': '20px', 'textAlign': 'center'})  # Display data here
        ])
    ])
])


@app.callback(
    Output('output-data', 'children'),
    [Input('base-currency', 'value'),
     Input('quote-currency', 'value')]
)
def update_data(base_currency, quote_currency):
    database_connection = DatabaseConnection()

    currency_series = database_connection.get_rates_as_series(
        base_currency,
        quote_currency,
    )

    fig = visualise_currency_series(currency_series)

    graph = dcc.Graph(
        figure=fig,
        style={'height': '600px'}  # Adjust graph height
    )
    return graph


@app.callback(
    Output('strategy-data', 'children'),
    [Input('base-currency', 'value'),
    Input('quote-currency', 'value'),
    Input('strategy', 'value')]
)
def update_data(base_currency, quote_currency, strategy):

    database_connection = DatabaseConnection()

    currency_series = database_connection.get_rates_as_series(
        base_currency,
        quote_currency,
    )

    profit_list = calculate_statistics(currency_series)
    investment = 1000
    annual_profit = calculate_annual_profit(profit_list, investment)

    fig = visualise_currency_series(currency_series)
    fig = add_profit_indicators(fig, profit_list)
    fig = add_title(fig, investment, annual_profit)

    graph = dcc.Graph(
        figure=fig,
        style={'height': '600px'}  # Adjust graph height
    )
    return graph


if __name__ == '__main__':
    app.run_server(debug=True)
