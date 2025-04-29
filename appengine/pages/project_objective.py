import dash
from dash import html

dash.register_page(__name__, path='/project_objective')

layout = html.Div([
    html.Div([
        html.H1('Project Objective', style={'textAlign': 'center'}),

        html.H2('Introduction', style={'marginTop': '30px'}),
        html.P(
            "Despite the depth of Pokémon’s competitive scene, there is no comprehensive dataset that systematically "
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
