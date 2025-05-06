import pandas as pd
import json
from google.cloud import storage
import io
import os

USE_GCS = os.environ.get('USE_GCS', '0') == '1'  # Default: use local files
BUCKET_NAME = 'cs163-group11.appspot.com'
POKEMON_BLOB = 'Pokemon.csv'
GEN9OU_BLOB = 'gen9ou_full_data.json'
POKEMON_LOCAL = 'components/data/Pokemon.csv'
GEN9OU_LOCAL = 'components/data/gen9ou_full_data.json'

def get_generation_to_region_mapping():
    return {
        1: 'Kanto', 2: 'Johto', 3: 'Hoenn', 4: 'Sinnoh',
        5: 'Unova', 6: 'Kalos', 7: 'Alola', 8: 'Galar', 9: 'Paldea'
    }

def get_stat_columns():
    return ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']

if USE_GCS:
    def load_pokemon_data():
        """Load Pokemon data from GCS bucket."""
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(POKEMON_BLOB)
        content = blob.download_as_string()
        return pd.read_csv(io.BytesIO(content))

    def load_gen9ou_data():
        """Load Gen 9 OU data from GCS bucket."""
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(GEN9OU_BLOB)
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

    def save_pokemon_data(df):
        """Save Pokemon data to GCS bucket."""
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(POKEMON_BLOB)
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        blob.upload_from_string(csv_buffer.getvalue(), content_type='text/csv')

    def save_gen9ou_data(df):
        """Save Gen 9 OU data to GCS bucket."""
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(GEN9OU_BLOB)
        json_buffer = io.StringIO()
        df.to_json(json_buffer, orient='records')
        blob.upload_from_string(json_buffer.getvalue(), content_type='application/json')

else:
    def load_pokemon_data():
        """Load Pokemon data from local file."""
        return pd.read_csv(POKEMON_LOCAL)

    def load_gen9ou_data():
        """Load Gen 9 OU data from local file."""
        with open(GEN9OU_LOCAL, 'r') as f:
            data = json.load(f)
        
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

    def save_pokemon_data(df):
        """Save Pokemon data to local file."""
        df.to_csv(POKEMON_LOCAL, index=False)

    def save_gen9ou_data(df):
        """Save Gen 9 OU data to local file."""
        with open(GEN9OU_LOCAL, 'w') as f:
            json.dump(df.to_dict('records'), f, indent=2) 