import dash
from dash import html

# Register the page
dash.register_page(__name__, path='/mock_recommender')

# --- Layout ---
layout = html.Div([
    html.H1("Pokémon Team Recommender", style={'textAlign': 'center', 'marginBottom': '30px'}),
    
    html.Div([
        html.Img(
            src='/assets/team_recommender.png',
            style={
                'width': '100%',
                'maxWidth': '800px',
                'display': 'block',
                'margin': '0 auto'
            }
        )
    ], style={
        'maxWidth': '1200px',
        'margin': '0 auto',
        'padding': '20px'
    })
])
