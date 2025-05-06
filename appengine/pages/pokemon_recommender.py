import dash
from dash import html, dcc, Input, Output, State, callback
import json
from components.model_utils import load_model_from_gcs, get_pokemon_info
from components.visualizations import create_move_usage_graph, create_counter_graph

# Load Pokemon data
with open("./components/data/gen9ou_full_data.json", "r") as f:
    pokemon_data = json.load(f)

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
            # Load cached or streamed model
            recommend = load_model_from_gcs()

            recommendation = recommend(pokemon1, pokemon2)

            p1_info = get_pokemon_info(pokemon1, pokemon_data)
            p2_info = get_pokemon_info(pokemon2, pokemon_data)

            if not p1_info or not p2_info:
                return "Error: One or both Pokemon not found.", {}, {}

            # Create visualizations
            move_fig = create_move_usage_graph(p1_info["moves"], pokemon1)
            counter_fig = create_counter_graph(p1_info["counters"], pokemon1)

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
            print(f"Error in update_output: {str(e)}")
            return html.Div([
                html.H3('Error:'),
                html.P(str(e))
            ]), {}, {}

    return '', {}, {}
