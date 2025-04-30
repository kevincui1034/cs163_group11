import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px
from google.cloud import storage
import io

# Register the page
dash.register_page(__name__, path='/')

# --- Load CSV from GCS ---
def load_pokemon_from_gcs():
    storage_client = storage.Client()
    bucket = storage_client.bucket('cs163-group11.appspot.com')
    blob = bucket.blob('Pokemon.csv')
    content = blob.download_as_string()
    df = pd.read_csv(io.BytesIO(content))
    return df

# Load the dataset
df = load_pokemon_from_gcs()

# --- Data Preparation ---
generation_to_region = {
    1: 'Kanto', 2: 'Johto', 3: 'Hoenn', 4: 'Sinnoh',
    5: 'Unova', 6: 'Kalos', 7: 'Alola', 8: 'Galar', 9: 'Paldea'
}
df['Region'] = df['Generation'].map(generation_to_region)

stat_cols = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
df['Total'] = df[stat_cols].sum(axis=1)

# --- Graph 1: Total Base Stats by Generation ---
mean_total_by_gen = df.groupby('Generation')['Total'].mean().reset_index()

fig_total_stats = px.scatter(
    mean_total_by_gen,
    x='Generation',
    y='Total',
    trendline='ols',
    title='Average Total Base Stats by Pokémon Generation',
    labels={'Total': 'Average Total Base Stats', 'Generation': 'Generation'}
)

# --- Graph 2: Correlation Heatmap Between Stats ---
correlation_matrix = df[stat_cols].corr()

fig_corr_heatmap = px.imshow(
    correlation_matrix,
    text_auto=True,
    title='Correlation Between Base Stats',
    labels=dict(color='Correlation', x='Stat', y='Stat')
)

# --- Layout ---
layout = html.Div([
    html.Div([
        html.H1('Finding the Best Pokémon', style={'textAlign': 'center'}),
        html.P(
            "Pokémon come in a vast array of forms, each with unique stats, typings, and abilities that contribute "
            "to their competitive viability. While the franchise spans multiple generations and regions, a key "
            "question remains: what truly defines a Pokémon's strength? Despite the competitive depth, there is "
            "no systematic, data-driven approach to understanding what makes a Pokémon effective in battle. "
            "This project bridges that gap by leveraging data science techniques to analyze how base stats, typings, "
            "abilities, and move pools influence competitive viability — and investigates regional and generational "
            "differences to see whether certain archetypes consistently exhibit superior traits.",
            style={'textAlign': 'center', 'maxWidth': '800px', 'margin': '20px auto'}
        ),
    ], style={
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center',
        'padding': '20px',
        'maxWidth': '1200px',
        'margin': '0 auto'
    }),

    html.Div([
        html.H2("Graphs Based on Pokémon Base Stats", style={'textAlign': 'center', 'marginTop': '50px'}),

        html.Div([
            html.H3("Average Total Base Stats by Generation"),
            dcc.Graph(figure=fig_total_stats),
            html.P(
                "One major question we explored was whether Pokémon generations show evidence of 'power creep'. "
                "Power creep refers to newer game additions becoming increasingly powerful compared to older ones. "
                "This scatter plot shows that as generations advance, the average total base stats of Pokémon increase. "
                "Generations 1–3 average around 400 total stats, while later generations such as Gen 6 approach 500. "
                "This insight is crucial for team building, suggesting that newer Pokémon tend to have stronger stat foundations."
            )
        ], style={'marginBottom': '60px'}),

        html.Div([
            html.H3("Correlation Heatmap Between Base Stats"),
            dcc.Graph(figure=fig_corr_heatmap),
            html.P(
                "This correlation heatmap reveals how different base stats interact. "
                "For example, high Speed tends not to correlate strongly with Special Defense. "
                "Players can use these insights during team building — if a player needs a high-HP Pokémon, "
                "the heatmap can guide what secondary stats (like Defense) are most complementary. "
                "Analyzing these correlations across generations also helps evaluate Pokémon viability across different metas."
            )
        ])
    ], style={
        'maxWidth': '1200px',
        'margin': '0 auto',
        'padding': '20px'
    })
])
