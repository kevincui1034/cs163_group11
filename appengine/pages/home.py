import dash
from dash import html, dcc
from components.data_loader import load_pokemon_data, get_generation_to_region_mapping, get_stat_columns
from components.visualizations import (
    create_total_stats_scatter, 
    create_correlation_heatmap, 
    create_total_stats_boxplot,
    create_stats_correlation_heatmap
)

# Register the page
dash.register_page(__name__, path='/')

# Load the dataset
df = load_pokemon_data()
df['Region'] = df['Generation'].map(get_generation_to_region_mapping())
stat_cols = get_stat_columns()

# Generate figures
fig_total_stats = create_total_stats_scatter(df, stat_cols)
fig_corr_heatmap = create_correlation_heatmap(df, stat_cols)
fig_boxplot = create_total_stats_boxplot(df, stat_cols)
fig_stats_heatmap = create_stats_correlation_heatmap(df, stat_cols)

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
            style={'textAlign': 'center', 'maxWidth': '800px', 'marginTop': '20px'}
        ),
    ], style={
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center',
        'padding': '10px',
        'maxWidth': '1200px',
        'margin': '0 auto'
    }),

    html.Div([
        html.H2("Graphs Based on Pokémon Base Stats", style={'textAlign': 'center', 'marginTop': '50px'}),

        html.Div([
            html.H3("Distribution of Total Base Stats by Generation"),
            dcc.Graph(figure=fig_boxplot, className='graph-style'),
        ], style={'marginBottom': '60px'}),

        html.Div([
            html.P(
                "One of our main questions was whether or not Pokemon generations were affected by 'power creep'. "
                "We define power creep as a process when newer additions to a video game can be used along older content, "
                "but the newer content are generally more powerful. With this distribution of stats by generation, "
                "we can see that newer Pokemon tend to have more total stat points than the older Pokemon. "
                "Gen 1-3 have around 400 total base stats, but the median number increases with each generation, "
                "with Gen 6 having about 500 total base stats. This is useful for determining a Pokemon's competitive "
                "viability when team building, as we can say that new Pokemon will tend to be stronger/have more base "
                "stats than older Pokemon."
            )
        ], style={'marginBottom': '60px', 'marginTop': '20px'}),
        
        html.Div([
            html.H3("Base Stats Correlation Heatmap"),
            dcc.Graph(figure=fig_stats_heatmap, className='graph-style'),
        ], style={'marginBottom': '60px', 'marginTop': '20px'}),
        
        html.Div([
            html.Div([
                html.P([
                    "This tells us what specific stat combinations we should focus on. ",
                    "For example, we can neglect a speedy Pokemon with high Special Defense."
                ], style={'marginBottom': '15px'}),
                html.P([
                    "We can see what specific combinations of Pokemon is relevant in terms of stats. ",
                    "Using this heatmap, we can also use this information on each generation to find if there is a correlation between Pokemon generations and usability."
                ], style={'marginBottom': '15px'}),
                html.P([
                    "This can also be used in Pokemon teambuilding, and if the player wants a high HP Pokemon, ",
                    "what would be the optimal second stat they should look for."
                ])
            ],)
        ])
    ], style={
        'maxWidth': '1200px',
        'margin': '0 auto',
        'padding': '20px'
    })
])
