import dash
from dash import html

# Register the page
dash.register_page(__name__, path='/mock_recommender')

# --- Layout ---
layout = html.Div([
    html.H1("Pokémon Team Recommender", style={'textAlign': 'center', 'marginBottom': '30px'}),
    
    html.Div([
        html.Img(
            src='assets/mock_recommend.png',
            style={
                'width': '100%',
                'height': 'auto',
                'display': 'block',
                'margin': '0 auto'
            }
        )
    ], style={
        'width': '100%',
        'margin': '0 auto',
        'padding': '20px'
    })
])
