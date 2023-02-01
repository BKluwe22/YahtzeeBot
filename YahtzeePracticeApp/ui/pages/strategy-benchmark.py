from dash import Dash, html, dcc, get_asset_url
import dash
import dash_bootstrap_components as dbc


dash.register_page(__name__, path="/strategy-benchmark-report")


layout = html.Div(
    children=[
        html.Iframe(
            src=get_asset_url('yahtzee-strategy-benchmark.html'),  # must be under assets/ to be properly served
            style={"height": "1080px", "width": "100%"},
        )
    ]
)
