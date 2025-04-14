
import pandas as pd
import glob

# Find all relevant CSVs
csv_files = glob.glob("**/*pokemon_usage_stats_with_gen.csv", recursive=True)

combined_df = pd.DataFrame()

for file in csv_files:
    df = pd.read_csv(file)
    df["Source File"] = file  # Optional: track which file each row came from
    combined_df = pd.concat([combined_df, df], ignore_index=True)

# Save combined result
combined_df.to_csv("combined_pokemon_usage.csv", index=False)
print(f"✅ Combined {len(csv_files)} files into 'combined_pokemon_usage.csv'")
