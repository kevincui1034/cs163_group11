from full_pokemon_parser import parse_all_pokemon
import json

# Read the latest gen9ou data file
with open("../data/2025-02-gen9ou-0.txt", "r") as f:
    raw = f.read()

# Parse the data
parsed = parse_all_pokemon(raw)

# Save to JSON
with open("../data/gen9ou_full_data.json", "w") as out:
    json.dump(parsed, out, indent=4)

print("Generated gen9ou_full_data.json successfully!") 