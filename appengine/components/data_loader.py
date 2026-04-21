import pandas as pd
import json
from google.cloud import storage
import io
import os
import tempfile

USE_GCS = os.environ.get('USE_GCS', '0') == '1'  # Default: use local files
# Prefer env (e.g. Vercel / other hosts); fall back to historical App Engine bucket.
BUCKET_NAME = os.environ.get('BUCKET_NAME', 'cs163-group11.appspot.com')


def _ensure_gcs_credentials():
    """
    Allow GCS auth on hosts without a credentials file path (e.g. Vercel).

    Set GCP_SERVICE_ACCOUNT_JSON to the raw JSON string of a service account
    that can read/write the bucket. If GOOGLE_APPLICATION_CREDENTIALS is
    already set, this is a no-op.
    """
    if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
        return
    raw = os.environ.get('GCP_SERVICE_ACCOUNT_JSON')
    if not raw:
        return
    path = os.path.join(tempfile.gettempdir(), 'vercel_gcp_sa.json')
    # Write once per cold start path (overwrite if env changed)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(raw)
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path


POKEMON_BLOB = 'Pokemon.csv'
GEN9OU_BLOB = 'gen9ou_full_data.json'
# Paths relative to this file so loads work when CWD is repo root (e.g. Vercel).
_COMPONENT_DIR = os.path.dirname(os.path.abspath(__file__))
POKEMON_LOCAL = os.path.join(_COMPONENT_DIR, 'data', 'Pokemon.csv')
GEN9OU_LOCAL = os.path.join(_COMPONENT_DIR, 'data', 'gen9ou_full_data.json')

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
        _ensure_gcs_credentials()
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(POKEMON_BLOB)
        content = blob.download_as_string()
        return pd.read_csv(io.BytesIO(content))

    def load_gen9ou_data():
        """Load Gen 9 OU data from GCS bucket."""
        _ensure_gcs_credentials()
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
        _ensure_gcs_credentials()
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(POKEMON_BLOB)
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        blob.upload_from_string(csv_buffer.getvalue(), content_type='text/csv')

    def save_gen9ou_data(df):
        """Save Gen 9 OU data to GCS bucket."""
        _ensure_gcs_credentials()
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