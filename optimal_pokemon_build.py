
import json

# Load the data
with open("pokemon_usage.json") as f:
    data = json.load(f)

# Build lookup dictionary
poke_lookup = {p['name']: p for p in data}

# Function to get optimal build
def get_optimal_build(pokemon_name):
    p = poke_lookup.get(pokemon_name)
    if not p:
        return f"{pokemon_name} not found in data."

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

# Example Usage
if __name__ == "__main__":
    pokemon_name = input("Enter Pokémon name: ")
    build = get_optimal_build(pokemon_name)
    for section, info in build.items():
        print(f"\n{section}:")
        if isinstance(info, list):
            for name, percent in info:
                print(f"  - {name}: {percent:.2f}%")
        else:
            print(f"  {info}")
