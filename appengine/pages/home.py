import dash
from dash import html, dcc
from components.data_loader import load_pokemon_from_gcs, get_generation_to_region_mapping, get_stat_columns
from components.visualizations import create_total_stats_scatter, create_correlation_heatmap

# Register the page
dash.register_page(__name__, path='/')

# Load the dataset
df = load_pokemon_from_gcs()
df['Region'] = df['Generation'].map(get_generation_to_region_mapping())
stat_cols = get_stat_columns()

# Generate figures
fig_total_stats = create_total_stats_scatter(df, stat_cols)
fig_corr_heatmap = create_correlation_heatmap(df, stat_cols)

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
