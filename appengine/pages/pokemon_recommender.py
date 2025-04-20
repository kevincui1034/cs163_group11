import dash
from dash import html, dcc, Input, Output, State, callback
import json
from pokemon_move_recommender import train_model, build_predictor


dash.register_page(__name__, path='/pokemon_recommender')
# Load the data and train the model
with open("gen9ou_full_data.json", "r") as f:
    pokemon_data = json.load(f)

clf, scaler, pca, df, data = train_model(pokemon_data)
recommend = build_predictor(clf, scaler, pca, data)

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
        html.Div(id='recommendation-output', style={'marginTop': 20})
    ])
])

@callback(
    Output('recommendation-output', 'children'),
    Input('recommend-button', 'n_clicks'),
    State('pokemon1-input', 'value'),
    State('pokemon2-input', 'value')
)
def update_output(n_clicks, pokemon1, pokemon2):
    if n_clicks > 0 and pokemon1 and pokemon2:
        try:
            recommendation = recommend(pokemon1, pokemon2)
            return html.Div([
                html.H3('Recommendation:'),
                html.P(recommendation)
            ])
        except Exception as e:
            return html.Div([
                html.H3('Error:'),
                html.P(str(e))
            ])
    return ''