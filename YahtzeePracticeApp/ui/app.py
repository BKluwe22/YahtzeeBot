from dash import Dash, html, dcc
import dash
import dash_bootstrap_components as dbc


app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.JOURNAL, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
    use_pages=True
)


app.layout = html.Div([
    
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(
                dcc.Link(f"{page['name']}", href=page["relative_path"], className="nav-link")
            ) for page in dash.page_registry.values()
        ],
        brand="Yahtzee Practice Application",
        brand_href="/",
        color="dark",
        dark=True,
        sticky='top'
    ),

	dash.page_container
])






if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=9000, debug=False)
    
    
    
    
    
    
    
    
