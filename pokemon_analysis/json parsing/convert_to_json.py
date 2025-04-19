import re
import json

def parse_pokemon_stats(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Split by Pokemon entries using the header pattern
    pokemon_sections = []
    matches = re.finditer(r'\+----------------------------------------\+\s+\|\s+([^|]+)\s*\|\s+\+----------------------------------------\+', content)
    
    start_positions = []
    names = []
    
    for match in matches:
        start_positions.append(match.start())
        names.append(match.group(1).strip())
    
    # Add end of file as the last position
    start_positions.append(len(content))
    
    # Extract each Pokemon section
    for i in range(len(names)):
        start = start_positions[i]
        end = start_positions[i + 1] if i + 1 < len(start_positions) else len(content)
        section = content[start:end]
        pokemon_sections.append((names[i], section))
    
    pokemon_data = []
    
    # Process each Pokemon section
    for name, section in pokemon_sections:
        # Create Pokemon data structure
        pokemon = {
            "name": name,
            "usage_stats": {},
            "abilities": {},
            "items": {},
            "spreads": {},
            "moves": {},
            "tera_types": {},
            "teammates": {},
            "checks_and_counters": {}
        }
        
        # Extract raw count
        raw_count_match = re.search(r'\|\s*Raw count:\s*(\d+)', section)
        if raw_count_match:
            pokemon["raw_count"] = int(raw_count_match.group(1))
        
        # Extract avg weight
        avg_weight_match = re.search(r'\|\s*Avg\.\s*weight:\s*([\d\.]+)', section)
        if avg_weight_match:
            pokemon["avg_weight"] = float(avg_weight_match.group(1))
        
        # Extract viability ceiling
        viability_match = re.search(r'\|\s*Viability Ceiling:\s*(\d+)', section)
        if viability_match:
            pokemon["viability_ceiling"] = int(viability_match.group(1))
        
        # Process each section
        # Abilities
        abilities_match = re.search(r'\|\s*Abilities\s*\|\s+\+----------------------------------------\+\s+(.*?)(?=\+----------------------------------------\+)', section, re.DOTALL)
        if abilities_match:
            for line in abilities_match.group(1).strip().split('\n'):
                match = re.search(r'\|\s*(.*?)\s+([\d\.]+)%', line)
                if match and "Other" not in match.group(1):
                    ability = match.group(1).strip()
                    percentage = float(match.group(2))
                    pokemon["abilities"][ability] = percentage
        
        # Items
        items_match = re.search(r'\|\s*Items\s*\|\s+\+----------------------------------------\+\s+(.*?)(?=\+----------------------------------------\+)', section, re.DOTALL)
        if items_match:
            for line in items_match.group(1).strip().split('\n'):
                match = re.search(r'\|\s*(.*?)\s+([\d\.]+)%', line)
                if match and "Other" not in match.group(1):
                    item = match.group(1).strip()
                    percentage = float(match.group(2))
                    pokemon["items"][item] = percentage
        
        # Spreads
        spreads_match = re.search(r'\|\s*Spreads\s*\|\s+\+----------------------------------------\+\s+(.*?)(?=\+----------------------------------------\+)', section, re.DOTALL)
        if spreads_match:
            for line in spreads_match.group(1).strip().split('\n'):
                match = re.search(r'\|\s*(.*?)\s+([\d\.]+)%', line)
                if match and "Other" not in match.group(1):
                    spread = match.group(1).strip()
                    percentage = float(match.group(2))
                    pokemon["spreads"][spread] = percentage
        
        # Moves
        moves_match = re.search(r'\|\s*Moves\s*\|\s+\+----------------------------------------\+\s+(.*?)(?=\+----------------------------------------\+)', section, re.DOTALL)
        if moves_match:
            for line in moves_match.group(1).strip().split('\n'):
                match = re.search(r'\|\s*(.*?)\s+([\d\.]+)%', line)
                if match and "Other" not in match.group(1):
                    move = match.group(1).strip()
                    percentage = float(match.group(2))
                    pokemon["moves"][move] = percentage
        
        # Tera Types
        tera_match = re.search(r'\|\s*Tera Types\s*\|\s+\+----------------------------------------\+\s+(.*?)(?=\+----------------------------------------\+)', section, re.DOTALL)
        if tera_match:
            for line in tera_match.group(1).strip().split('\n'):
                match = re.search(r'\|\s*(.*?)\s+([\d\.]+)%', line)
                if match and "Other" not in match.group(1):
                    tera = match.group(1).strip()
                    percentage = float(match.group(2))
                    pokemon["tera_types"][tera] = percentage
        
        # Teammates
        teammates_match = re.search(r'\|\s*Teammates\s*\|\s+\+----------------------------------------\+\s+(.*?)(?=\+----------------------------------------\+)', section, re.DOTALL)
        if teammates_match:
            for line in teammates_match.group(1).strip().split('\n'):
                match = re.search(r'\|\s*(.*?)\s+([\d\.]+)%', line)
                if match:
                    teammate = match.group(1).strip()
                    percentage = float(match.group(2))
                    pokemon["teammates"][teammate] = percentage
        
        # Checks and Counters - special format
        cc_match = re.search(r'\|\s*Checks and Counters\s*\|\s+\+----------------------------------------\+\s+(.*?)(?=(?:\+----------------------------------------\+|$))', section, re.DOTALL)
        if cc_match:
            cc_text = cc_match.group(1).strip()
            if cc_text:  # Non-empty section
                lines = cc_text.split('\n')
                for line in lines:
                    # Match the score pattern: "Pokémon score (mean±deviation)"
                    score_match = re.search(r'\|\s*(.*?)\s+([\d\.]+)\s+\(([\d\.]+)±([\d\.]+)\)', line)
                    if score_match:
                        counter_name = score_match.group(1).strip()
                        score = float(score_match.group(2))
                        mean = float(score_match.group(3))
                        deviation = float(score_match.group(4))
                        
                        counter_data = {
                            "score": score,
                            "mean": mean, 
                            "deviation": deviation
                        }
                        
                        # Check if the line contains KOed/switched info
                        koed_switched = re.search(r'\|\s*\(([\d\.]+)%\s+KOed\s+/\s+([\d\.]+)%\s+switched out\)', line)
                        if koed_switched:
                            counter_data["koed_percent"] = float(koed_switched.group(1))
                            counter_data["switched_percent"] = float(koed_switched.group(2))
                        
                        pokemon["checks_and_counters"][counter_name] = counter_data
        
        pokemon_data.append(pokemon)
    
    return pokemon_data

# Convert the top Pokémon data to JSON
try:
    pokemon_data = parse_pokemon_stats('gen9ou-0_top.txt')
    with open('gen9ou-0_top.json', 'w') as outfile:
        json.dump(pokemon_data, outfile, indent=2)
    print('Successfully converted gen9ou-0_top.txt to gen9ou-0_top.json')
    print(f'Converted {len(pokemon_data)} Pokémon entries')
except Exception as e:
    print(f'Error during conversion: {str(e)}') 