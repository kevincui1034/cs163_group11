import dash
from dash import html, dcc, Input, Output, State, callback
import json
import tempfile
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from google.cloud import storage
from components.pokemon_move_recommender import build_predictor


### ONLY FOR LOCAL
### TOO BIG FOR CLOUD

with open("./components/data/gen9ou_full_data.json", "r") as f:
    pokemon_data = json.load(f)

# Global model cache
clf = scaler = pca = df = data = recommend = None
model_loaded = False

# 🔹 GCS model loading logic
def load_model_from_gcs():
    global clf, scaler, pca, df, data, recommend, model_loaded

    if model_loaded:
        return recommend

    print("[INFO] Loading model from GCS...")

    bucket_name = "cs163-group11.appspot.com"  # 🔁 Replace with your actual bucket name
    blob_path = "models/pokemon_model.pkl"

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)

    with tempfile.NamedTemporaryFile() as temp_file:
        blob.download_to_filename(temp_file.name)
        with open(temp_file.name, "rb") as f:
            clf, scaler, pca, df, data = pickle.load(f)

    recommend = build_predictor(clf, scaler, pca, data)
    model_loaded = True
    print("[INFO] Model loaded and ready from GCS.")

    return recommend

# Pokémon info helper
def get_pokemon_info(pokemon_name):
    pokemon = next((p for p in pokemon_data if p["Pokemon"] == pokemon_name), None)
    if not pokemon:
        return None
    
    return {
        "moves": pokemon.get("Moves", {}),
        "counters": pokemon.get("Checks and Counters", []),
        "raw_count": pokemon.get("Raw Count", 0),
        "viability_ceiling": pokemon.get("Viability Ceiling", 0)
    }

# Register Dash page
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
            # 🔹 Load cached or streamed model
            recommend = load_model_from_gcs()

            recommendation = recommend(pokemon1, pokemon2)

            p1_info = get_pokemon_info(pokemon1)
            p2_info = get_pokemon_info(pokemon2)

            if not p1_info or not p2_info:
                return "Error: One or both Pokemon not found.", {}, {}

            # Move usage graph
            moves_df = pd.DataFrame(list(p1_info["moves"].items()), columns=['Move', 'Usage %'])
            move_fig = px.bar(moves_df, x='Move', y='Usage %',
                              title=f'{pokemon1} Move Usage',
                              color='Usage %',
                              color_continuous_scale='Viridis')

            # Counter graph
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
