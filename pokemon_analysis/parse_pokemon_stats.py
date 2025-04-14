import re
import csv
import os

def parse_pokemon_stats():
    try:
        # Get the current script's directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        input_file = os.path.join(script_dir, "2023-02-gen9ou-0.txt")
        output_file = os.path.join(script_dir, "2023-02-pokemon_usage_stats.csv")
        
        print(f"Script directory: {script_dir}")
        print(f"Input file: {input_file}")
        print(f"Output file: {output_file}")
        
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"Read {len(lines)} lines from input file")
        
        # Prepare CSV data
        csv_data = []
        headers = ['Rank', 'Pokemon', 'Usage %', 'Raw Count', 'Raw %', 'Real Count', 'Real %']
        csv_data.append(headers)
        
        # Process each line
        matches_found = 0
        for line in lines:
            # Skip empty lines, separators, and headers
            if not line.strip() or '+----+' in line or '| Rank |' in line:
                continue
            
            # Try to extract data using split
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 8:  # We expect 8 parts (including empty strings at start/end)
                try:
                    rank = parts[1].strip()
                    pokemon = parts[2].strip()
                    usage_pct = parts[3].strip().rstrip('%')
                    raw_count = parts[4].strip()
                    raw_pct = parts[5].strip().rstrip('%')
                    real_count = parts[6].strip()
                    real_pct = parts[7].strip().rstrip('%')
                    
                    # Only process if we have a valid rank number
                    if rank.isdigit():
                        matches_found += 1
                        csv_data.append([
                            rank,
                            pokemon,
                            usage_pct,
                            raw_count,
                            raw_pct,
                            real_count,
                            real_pct
                        ])
                except Exception as e:
                    print(f"Warning: Could not parse line: {line.strip()}")
                    print(f"Error: {str(e)}")
        
        print(f"Found {matches_found} Pokemon entries")
        
        # Write to CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)
        
        print(f"Successfully wrote {len(csv_data)} rows to {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    parse_pokemon_stats() 