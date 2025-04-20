import dash
from dash import html, dcc, Input, Output, State, callback
import json
import os
import pickle
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from components.pokemon_move_recommender import build_predictor

# Load Pokémon data for context/display (not training)
with open("./components/data/gen9ou_full_data.json", "r") as f:
    pokemon_data = json.load(f)

# ✅ Load pre-trained model from pickle
with open(os.path.join("models", "pokemon_model.pkl"), "rb") as f:
    clf, scaler, pca, df, data = pickle.load(f)

# ✅ Build the predictor
recommend = build_predictor(clf, scaler, pca, data)

# Get Pokémon info
def get_pokemon_info(pokemon_name):
    pokemon = next((p for p in pokemon_data if p["Pokemon"] == pokemon_name), None)
    if not pokemon:
        return None
    
    moves = pokemon.get("Moves", {})
    counters = pokemon.get("Checks and Counters", [])
    
    return {
        "moves": moves,
        "counters": counters,
        "raw_count": pokemon.get("Raw Count", 0),
        "viability_ceiling": pokemon.get("Viability Ceiling", 0)
    }

dash.register_page(__name__, path='/pokemon_recommender')

layout = html.Div([
    html.H1('Pokemon Move Recommender'),
    html.Div([
        html.Label('Your Pokemon:'),
        dcc.Input(id='pokemon1-input', type='text', placeholder='Enter Pokemon name'),
        html.Br(),
        html.Label('Opponent Pokemon:'),
        dcc.Input(id='pokemon2-input', type='text', placeholder='Enter Pokemon name'),
        html.Br(),
        html.Button('Get Recommendation', id='recommend-button', n_clicks=0),
    ]),
    html.Div(id='recommendation-output', style={'marginTop': 20}),
    html.Div([
        dcc.Graph(id='move-usage-graph'),
        dcc.Graph(id='counter-graph')
    ], style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-around'})
])

@callback(
    [Output('recommendation-output', 'children'),
     Output('move-usage-graph', 'figure'),
     Output('counter-graph', 'figure')],
    Input('recommend-button', 'n_clicks'),
    State('pokemon1-input', 'value'),
    State('pokemon2-input', 'value')
)
def update_output(n_clicks, pokemon1, pokemon2):
    if n_clicks > 0 and pokemon1 and pokemon2:
        try:
            recommendation = recommend(pokemon1, pokemon2)
            
            p1_info = get_pokemon_info(pokemon1)
            p2_info = get_pokemon_info(pokemon2)
            
            if not p1_info or not p2_info:
                return "Error: One or both Pokemon not found.", {}, {}
            
            moves_df = pd.DataFrame(list(p1_info["moves"].items()), columns=['Move', 'Usage %'])
            move_fig = px.bar(moves_df, x='Move', y='Usage %', 
                              title=f'{pokemon1} Move Usage',
                              color='Usage %',
                              color_continuous_scale='Viridis')
            
            counters_df = pd.DataFrame(p1_info["counters"])
            if not counters_df.empty:
                counter_fig = go.Figure(data=[
                    go.Bar(name='KO %', x=counters_df['Name'], y=counters_df['KOed']),
                    go.Bar(name='Switch %', x=counters_df['Name'], y=counters_df['Switched Out'])
                ])
                counter_fig.update_layout(
                    title=f'{pokemon1} Counters',
                    barmode='group',
                    xaxis_title='Counter Pokemon',
                    yaxis_title='Percentage'
                )
            else:
                counter_fig = go.Figure()
                counter_fig.add_annotation(text="No counter data available",
                                           xref="paper", yref="paper",
                                           x=0.5, y=0.5, showarrow=False)
            
            recommendation_output = html.Div([
                html.H3('Recommendation:'),
                html.P(recommendation),
                html.H4('Pokemon Details:'),
                html.Div([
                    html.Div([
                        html.H5(f'{pokemon1} Stats:'),
                        html.P(f'Raw Count: {p1_info["raw_count"]}'),
                        html.P(f'Viability Ceiling: {p1_info["viability_ceiling"]}'),
                    ], style={'marginRight': '20px'}),
                    html.Div([
                        html.H5(f'{pokemon2} Stats:'),
                        html.P(f'Raw Count: {p2_info["raw_count"]}'),
                        html.P(f'Viability Ceiling: {p2_info["viability_ceiling"]}'),
                    ])
                ], style={'display': 'flex', 'justifyContent': 'space-around'})
            ])
            
            return recommendation_output, move_fig, counter_fig
            
        except Exception as e:
            return html.Div([
                html.H3('Error:'),
                html.P(str(e))
            ]), {}, {}
    return '', {}, {}
