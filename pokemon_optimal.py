import json

with open("pokemon_usage.json") as f:
    data = json.load(f)

# Create dictionary to access by Pokémon name
poke_lookup = {p['name']: p for p in data}
def get_optimal_build(pokemon_name):
    p = poke_lookup.get(pokemon_name)
    if not p:
        return f"{pokemon_name} not found in data."

    # Extract top teammates, moves, items, tera types, counters
    def top_n(d, n=5):
        return sorted(d.items(), key=lambda x: x[1], reverse=True)[:n]

    teammates = top_n(p.get('teammates', {}))
    moves = top_n(p.get('moves', {}))
    items = top_n(p.get('items', {}))
    tera = top_n(p.get('tera_types', {}))
    counters = top_n(p.get('checks_and_counters', {}))

    return {
        "Pokémon": pokemon_name,
        "Top Moves": moves,
        "Top Items": items,
        "Top Tera Types": tera,
        "Top Teammates": teammates,
        "Counters": counters if counters else "No counter data available"
    }
build = get_optimal_build("Iron Valiant")
for section, info in build.items():
    print(f"{section}:\n", info, "\n")
