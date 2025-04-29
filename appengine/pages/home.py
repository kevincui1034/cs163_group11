import dash
from dash import html

dash.register_page(__name__, path='/')

layout = html.Div([
    html.Div([
        html.H1('Finding the best Pokemon', style={'textAlign': 'center'}),
        html.Div('Pokémon come in a vast array of forms, each with unique stats, typings, \
            and abilities that contribute to their competitive viability. While the Pokémon \
            franchise spans multiple generations and regions, a key question remains: what truly\
            defines a Pokémon\s strength? While players and analysts engage deeply with the\
            competitive scene, there is no systematic, data-driven approach to understanding\
            what makes a Pokémon truly effective in battle. This project aims to bridge that gap\
            by leveraging data science techniques to analyze how attributes such as base stats,\
            typings, abilities, and move pools influence competitive viability. Additionally,\
            we will investigate regional and generational differences, exploring how Pokémon\
            vary based on their origin and whether certain archetypes consistently exhibit superior competitive traits.', 
                style={'textAlign': 'center', 'maxWidth': '800px', 'margin': '0 auto'}),
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