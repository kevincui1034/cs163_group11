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

            html.H2("What is Smogon and the OU Tier?", style={'marginTop': '40px'}),
            html.P([
                "Smogon is the leading competitive Pokémon community, known for creating and maintaining a widely respected battle tiering system. ",
                "It provides in-depth strategy guides, analysis, and statistics for competitive battling. You can visit Smogon's main site ",
                html.A("here", href="https://www.smogon.com/", target="_blank"), "."
            ]),
            html.P([
                "One of Smogon's most popular tiers is OU, or OverUsed. The OU tier includes Pokémon that are frequently used in standard competitive play. ",
                "It strikes a balance between power and variety, excluding the most dominant 'Uber' Pokémon while still allowing a wide range of viable strategies. ",
                "OU is the central metagame tier used in Pokémon Showdown ladder matches, tournaments, and analysis. More about Smogon’s tiering system can be found ",
                html.A("here", href="https://www.smogon.com/tiers/", target="_blank"), "."
            ]),

            html.H2("How Are Pokémon Placed in the OU Tier?", style={'marginTop': '40px'}),
            html.P("Pokémon are placed in the OU tier based on competitive usage data collected from Pokémon Showdown. Here’s how the process works:"),
            html.Ul([
                html.Li("Usage Threshold: If a Pokémon is used in at least 4.52% of high-level standard battles (e.g., 1695+ Elo) during a tiering period (usually monthly), it qualifies as OU."),
                html.Li("Statistical Rollover: If usage drops below the threshold for several months, the Pokémon may fall to a lower tier like UU (UnderUsed). Conversely, rising usage can promote a Pokémon to OU."),
                html.Li("Suspect Tests: Sometimes, Pokémon are voted on by the community via suspect tests if they are considered overpowered or unhealthy for the meta."),
                html.Li("Quickbans and Council Decisions: The OU council can issue quickbans to immediately remove problematic Pokémon or mechanics even outside of usage considerations."),
            ], style={'textAlign': 'left', 'margin': '20px auto', 'maxWidth': '700px'}),

            html.P([
                "For example, if Kingambit is used in 7% of battles in January, it remains OU. But if its usage falls to 3.8% for multiple months, it could drop to UU unless it's banned or kept due to other factors. ",
                "You can view current usage statistics ",
                html.A("here", href="https://www.smogon.com/stats/", target="_blank"), "."
            ]),
        ], style={'textAlign': 'center', 'maxWidth': '800px', 'margin': '0 auto'}),
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
