import pandas as pd
import json
from google.cloud import storage
import io

def load_pokemon_from_gcs():
    storage_client = storage.Client()
    bucket = storage_client.bucket('cs163-group11.appspot.com')
    blob = bucket.blob('Pokemon.csv')
    content = blob.download_as_string()
    df = pd.read_csv(io.BytesIO(content))
    return df

def load_gen9ou_data():
    storage_client = storage.Client()
    bucket = storage_client.bucket('cs163-group11.appspot.com')
    blob = bucket.blob('gen9ou_full_data.json')
    content = blob.download_as_string()
    data = json.loads(content)
    
    rows = []
    for entry in data:
        pokemon = entry['Pokemon']
        viability = entry.get('Viability Ceiling', 0)
        teammates = entry.get('Teammates', {})
        teammate_list = [teammate for teammate in teammates.keys()]
        rows.append({
            'Pokemon': pokemon,
            'Viability': viability,
            'Teammates': ' '.join(teammate_list)
        })
    return pd.DataFrame(rows)

def get_generation_to_region_mapping():
    return {
        1: 'Kanto', 2: 'Johto', 3: 'Hoenn', 4: 'Sinnoh',
        5: 'Unova', 6: 'Kalos', 7: 'Alola', 8: 'Galar', 9: 'Paldea'
    }

def get_stat_columns():
    return ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'] 