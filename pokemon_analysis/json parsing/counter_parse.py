import json
import re
import pandas as pd

# Load the JSON file
with open("gen9ou_full_data.json") as f:
    data = json.load(f)

# Parse out counter names and their associated numbers
parsed_data = []

for pkmn in data:
    name = pkmn.get("Pokemon", "")
    counters = pkmn.get("Checks and Counters", [])
    for c in counters:
        raw_name = c["Name"]
        match = re.match(r"^(.*) (\d+\.\d+)$", raw_name)
        if match:
            counter_name = match.group(1)
            counter_number = float(match.group(2))
            parsed_data.append({
                "Target Pokemon": name,
                "Counter Pokemon": counter_name,
                "Score": counter_number,
                "KOed": c["KOed"],
                "Switched Out": c["Switched Out"]
            })

# Convert to DataFrame and preview
df = pd.DataFrame(parsed_data)
print(df.info())
