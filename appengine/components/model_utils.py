import tempfile
import pickle
from google.cloud import storage
from components.pokemon_move_recommender import build_predictor

# Global model cache
clf = scaler = pca = df = data = recommend = None
model_loaded = False

def load_model_from_gcs():
    global clf, scaler, pca, df, data, recommend, model_loaded

    if model_loaded:
        return recommend

    print("[INFO] Loading model from GCS...")

    bucket_name = "cs163-group11.appspot.com"
    blob_path = "models/pokemon_model.pkl"

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)

    with tempfile.NamedTemporaryFile() as temp_file:
        blob.download_to_filename(temp_file.name)
        with open(temp_file.name, "rb") as f:
            clf, scaler, pca, df, data = pickle.load(f)

    recommend = build_predictor(clf, scaler, pca, data)
    model_loaded = True
    print("[INFO] Model loaded and ready from GCS.")

    return recommend

def get_pokemon_info(pokemon_name, pokemon_data):
    pokemon = next((p for p in pokemon_data if p["Pokemon"] == pokemon_name), None)
    if not pokemon:
        return None
    
    return {
        "moves": pokemon.get("Moves", {}),
        "counters": pokemon.get("Checks and Counters", []),
        "raw_count": pokemon.get("Raw Count", 0),
        "viability_ceiling": pokemon.get("Viability Ceiling", 0)
    } 