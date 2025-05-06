import dash
from dash import html, dcc, callback, Input, Output
from components.data_loader import load_gen9ou_data, load_pokemon_data, get_generation_to_region_mapping, get_stat_columns
from components.visualizations import create_team_archetype_visuals, create_correlation_heatmap, create_total_stats_scatter

# Register page
dash.register_page(__name__, path='/major_findings')

# Load data
df_gen9ou = load_gen9ou_data()
df_stats = load_pokemon_data()
df_stats['Region'] = df_stats['Generation'].map(get_generation_to_region_mapping())
stat_cols = get_stat_columns()

# Generate figures
fig_cluster, fig_viability = create_team_archetype_visuals(df_gen9ou)
heatmap_fig = create_correlation_heatmap(df_stats, stat_cols)
scatter_fig = create_total_stats_scatter(df_stats, stat_cols)

# --- Layout ---
layout = html.Div([
    html.H1("Major Findings", style={'textAlign': 'center', 'marginBottom': '30px'}),

    html.Div([
        html.H2("Team Archetype Analysis", style={'textAlign': 'center'}),
        html.P("Our analysis of Pokémon team compositions reveals four distinct team archetypes based on teammate relationships:", style={'textAlign': 'center'}),
        html.Ul([
            html.Li([html.Strong("Bulky Offense:"), " Teams combining defensive walls with powerful attackers."], style={'textAlign': 'center'}),
            html.Li([html.Strong("Hyper Offense:"), " Teams focused on speed control and powerful sweepers."], style={'textAlign': 'center'}),
            html.Li([html.Strong("Balanced Teams:"), " Teams with a mix of support, pivots, and hazard control."], style={'textAlign': 'center'}),
            html.Li([html.Strong("Stall/Fat Balance:"), " Teams built around regeneration cores and defensive tanks."], style={'textAlign': 'center'})
        ], style={'textAlign': 'center', 'listStyle': 'none', 'padding': '0'}),
        dcc.Graph(figure=fig_cluster, className='graph-style')
    ], style={'marginBottom': '70px', 'textAlign': 'center'}),

    html.Div([
        html.H2("Viability Analysis", style={'textAlign': 'center'}),
        html.P("The visualization below shows the relationship between team archetypes and their average viability scores.", style={'textAlign': 'center'}),
        dcc.Graph(figure=fig_viability, className='graph-style')
    ], style={'marginBottom': '70px', 'textAlign': 'center'}),

    html.Div([
        html.H2("Average Base Stats by Generation", style={'textAlign': 'center'}),
        dcc.Graph(figure=scatter_fig, className='graph-style'),
    ], style={'marginBottom': '70px', 'textAlign': 'center'}),
    
    html.Div([
        html.P(
            "Each point represents the mean total base stat for a specific generation. "
            "The upward slope of the regression line suggests a power creep trend—a gradual increase in average stat totals over time. "
            "Generation 6 appears to have a particularly high average, likely due to the introduction of Mega Evolutions. "
            "Future generations do not have this sort of spike in total base stats, but they have more than the first five generations. "
            "This graph may support the hypothesis that power creep does play a role in Pokemon regarding base stats. "
            "Notice the red area around the red line, representing the confidence interval of the linear regression. "
            "The line gets narrower around Generations 4,5,6 and wider in the later Generations. "
            "The model is fairly confident in the middle generations, where there are more data points, "
            "and slightly less confident at the extremes (Gen 1 and Gen 9).",
            style={'textAlign': 'center'}
        )
    ], style={'marginBottom': '70px', 'textAlign': 'center'}),
    
    html.Hr()
], style={
    'maxWidth': '1200px',
    'margin': '0 auto',
    'padding': '20px',
    'textAlign': 'center'
})
