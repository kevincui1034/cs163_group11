import dash
from dash import html

dash.register_page(__name__, path='/data')

layout = html.Div([
    html.Div([
        html.H1('Data Page', style={'textAlign': 'center'}),

        html.Div([
            html.P("We collected our data from a variety of sources. The major datasets we looked at were from Smogon and Kaggle."),
            html.P("Within Smogon, we used competitive usage statistics, checks and counters, and sample sets from top-tier Pokémon."),
            html.P("Kaggle provided structured Pokémon datasets including base stats, types, generations, and move pools."),
            html.P("These sources allowed us to analyze how attributes like typing, base stats, and generation affect competitive performance."),
        ], style={'textAlign': 'center', 'maxWidth': '800px', 'margin': '0 auto'})
    ], style={
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center',
        'minHeight': '80vh',
        'padding': '20px',
        'maxWidth': '1200px',
        'margin': '0 auto'
    })
])
