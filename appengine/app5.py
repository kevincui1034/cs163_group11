import dash
from dash import Dash, html
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY, '/assets/custom.css'])

server = app.server

# --- Navbar ---
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Project Objective", href="/project_objective")),
        dbc.NavItem(dbc.NavLink("Analytical Methods", href="/analytical_methods")),
        dbc.NavItem(dbc.NavLink("Major Findings", href="/major_findings")),
        # Fix or comment out the recommender if not ready
        # dbc.NavItem(dbc.NavLink("Pokemon Recommender", href="/pokemon_recommender")),
    ],
    brand=html.Span("What Makes a Good Pokémon?", style={'fontSize': '24px', 'fontWeight': 'bold'}),
    brand_href="/",
    color="dark",
    dark=True,
)

# --- Footer ---
footer = dbc.Container(
    dbc.Row(
        [
            dbc.Col(html.Div([
                html.A("GitHub", href="https://github.com/kevincui1034/cs163_group11", target="_blank"),
                html.Span(" | © 2025 CS163 Group 11")
            ], style={'textAlign': 'center', 'padding': '10px'}))
        ]
    ),
    className="footer",
    fluid=True,
)

# --- App Layout ---
app.layout = html.Div([
    navbar,
    html.Div(style={'height': '20px'}),  # small spacer between navbar and page
    dash.page_container,
    footer,
])

if __name__ == '__main__':
    app.run(debug=True)
