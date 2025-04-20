import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY, '/assets/custom.css'])


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Data", href="/data")),
        dbc.NavItem(dbc.NavLink("Graphs", href="/graphs")),
        dbc.NavItem(dbc.NavLink("Pokemon Recommender", href="/pokemon_recommender")),
    ],
    brand=html.Span("What makes a good Pokemon?", style={'fontSize': '24px', 'fontWeight': 'bold'}),
    brand_href="/",
    color="dark",
    dark=True,
)

footer = dbc.Container(
    dbc.Row(
        [
            dbc.Col(html.A("Github", href="https://github.com/kevincui1034/cs163_group11"), align="left"),
        ],
    ),
    className="footer",
    fluid=True,
)

app.layout = html.Div([
    navbar,
    dash.page_container,
    footer,
])

if __name__ == '__main__':
    app.run(debug=True)