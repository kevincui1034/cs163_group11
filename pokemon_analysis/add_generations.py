import csv
import os

def create_pokemon_generation_map(pokemon_csv_path):
    """Create a mapping of Pokemon names to their generations."""
    pokemon_generations = {}
    
    with open(pokemon_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['Name'].strip()
            form = row['Form'].strip()
            generation = row['Generation']
            
            # Handle Pokemon with forms
            if form:
                full_name = f"{name}-{form}"
            else:
                full_name = name
                
            pokemon_generations[full_name] = generation
            
            # Also add the base name without form
            if form:
                pokemon_generations[name] = generation
    
    return pokemon_generations

def add_generation_to_stats(input_file, output_file, pokemon_generations):
    """Add generation column to usage stats file."""
    rows = []
    
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames + ['Generation']
        
        for row in reader:
            pokemon_name = row['Pokemon']
            
            # Try to find the generation
            generation = pokemon_generations.get(pokemon_name)
            if not generation:
                # Try removing any form suffix
                base_name = pokemon_name.split('-')[0]
                generation = pokemon_generations.get(base_name)
            
            row['Generation'] = generation or 'Unknown'
            rows.append(row)
    
    # Write the output file
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def main():
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define file paths
    pokemon_csv = os.path.join(script_dir, 'Pokemon.csv')
    stats_2023 = os.path.join(script_dir, '2023-02-pokemon_usage_stats.csv')
    stats_2024 = os.path.join(script_dir, '2024-02-pokemon_usage_stats.csv')
    stats_2025 = os.path.join(script_dir, '2025-02-pokemon_usage_stats.csv')
    output_2023 = os.path.join(script_dir, '2023-02-pokemon_usage_stats_with_gen.csv')
    output_2024 = os.path.join(script_dir, '2024-02-pokemon_usage_stats_with_gen.csv')
    output_2025 = os.path.join(script_dir, '2025-02-pokemon_usage_stats_with_gen.csv')

    # Create Pokemon generation mapping
    print("Creating Pokemon generation mapping...")
    pokemon_generations = create_pokemon_generation_map(pokemon_csv)
    
    # Process 2023 stats
    print("Processing 2023 stats...")
    add_generation_to_stats(stats_2023, output_2023, pokemon_generations)
    
    # Process 2024 stats
    print("Processing 2024 stats...")
    add_generation_to_stats(stats_2024, output_2024, pokemon_generations)

    # Process 2025 stats
    print("Processing 2025 stats...")
    add_generation_to_stats(stats_2025, output_2025, pokemon_generations)
    
    print("Done! New files created with generation information.")

if __name__ == "__main__":
    main() 