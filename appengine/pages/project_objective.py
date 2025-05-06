import dash
from dash import html

dash.register_page(__name__, path='/project_objective')

layout = html.Div([
    html.Div([
        html.H1('Project Objective', style={'textAlign': 'center'}),

        html.H2('Introduction', style={'marginTop': '30px'}),
        html.P(
            "Despite the depth of Pokémon's competitive scene, there is no comprehensive dataset that systematically "
            "explores Pokémon attributes in a way similar to how scientists study animal species and ecosystems. "
            "With this information, it can be used for fans and players to understand the inner workings of the Pokémon world, "
            "and gain a better understanding of how the developers designed the game environment. "
            "This project seeks to fill that gap by:"
        ),
        html.Ul([
            html.Li("Providing data-driven insights into Pokémon design, helping fans and analysts understand patterns behind competitive viability."),
            html.Li("Assisting competitive players in team-building by identifying Pokémon with optimal stat distributions and move combinations."),
            html.Li("Contributing to discussions on game balancing, such as whether newer generations introduce 'power creep' that skews competition."),
            html.Li("Offering a structured framework that could be expanded upon in future Pokémon research, such as analyzing team synergy, meta shifts, or battle strategies."),
        ], style={'maxWidth': '900px'}),

        html.H2('Data Sources', style={'marginTop': '30px'}),
        html.Ul([
            html.Li(html.A('ArmGilles - Pokémon Dataset (GitHub Gist)', href="https://gist.github.com/armgilles/194bcff35001e7eb53a2a8b441e8b2c6", target="_blank")),
            html.Li(html.A('CalebReigada - Pokémon Dataset (Kaggle)', href="https://www.kaggle.com/datasets/calebreigada/pokemon", target="_blank")),
            html.Li(html.A('Netzuel - Pokémon GO Dataset: 15 Generations (Kaggle)', href="https://www.kaggle.com/datasets/netzuel/pokmon-go-dataset-15-generations", target="_blank")),
            html.Li(html.A('Pokémon Game Info - Move Data', href="https://pokemon.gameinfo.io/en/moves", target="_blank")),
            html.Li(html.A('Pokémon Showdown - Pokémon Set Data', href="https://play.pokemonshowdown.com/data/sets/", target="_blank")),
            html.Li(html.A('Smogon - Pokémon Competitive Statistics', href="https://www.smogon.com/stats/", target="_blank")),
            html.Li(html.A('Thiago Amancio - Full Pokémon and Moves Datasets (Kaggle)', href="https://www.kaggle.com/datasets/thiagoamancio/full-pokemons-and-moves-datasets?select=metadata_pokemon_moves.csv", target="_blank")),
        ], style={'maxWidth': '900px'}),

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
                "OU is the central metagame tier used in Pokémon Showdown ladder matches, tournaments, and analysis. More about Smogon's tiering system can be found ",
                html.A("here", href="https://www.smogon.com/tiers/", target="_blank"), "."
            ]),

            html.H2("How Are Pokémon Placed in the OU Tier?", style={'marginTop': '40px'}),
            html.P("Pokémon are placed in the OU tier based on competitive usage data collected from Pokémon Showdown. Here's how the process works:"),
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
            
        html.H2('Expected Major Findings', style={'marginTop': '30px'}),
        html.Ul([
            html.Li("A correlation between Pokémon stats and their originating region."),
            html.Li("Certain archetypes of Pokémon (e.g., Fire-types) may show predisposition toward higher specific attributes like Attack."),
            html.Li("Later generations of Pokémon show signs of 'power creep', with trends in which stats (e.g., Attack, Speed) are increasingly inflated."),
            html.Li("An assessment of whether rarer Pokémon consistently exhibit superior stats or unique move combinations."),
            html.Li("Regional biases where specific types (like Water-types) are more dominant in certain areas."),
        ], style={'maxWidth': '900px'}),

    ], style={
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center',
        'padding': '20px',
        'maxWidth': '1200px',
        'margin': '0 auto'
    })
])
