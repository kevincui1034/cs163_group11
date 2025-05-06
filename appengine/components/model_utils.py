import tempfile
import pickle
from google.cloud import storage
from components.pokemon_move_recommender import build_predictor

# Global model cache
clf = scaler = pca = df = data = recommend = None
model_loaded = False

def load_model_from_gcs():
    """Load the model from local file."""
    from components.pokemon_move_recommender import load_model, build_predictor
    import json
    
    # Load data and model
    with open("./components/data/gen9ou_full_data.json", "r") as f:
        pokemon_data = json.load(f)
    
    # Load model data (model, scaler, pca, df, data)
    model_data = load_model()
    if not isinstance(model_data, tuple) or len(model_data) != 5:
        raise ValueError(f"Invalid model data format. Expected tuple with 5 elements, got {type(model_data)} with {len(model_data) if isinstance(model_data, tuple) else 'N/A'} elements")
    
    model, scaler, pca, _, _ = model_data  # Only need first 3 elements
    
    # Create and return predictor
    return build_predictor(model, scaler, pca, pokemon_data)

def get_pokemon_info(pokemon_name, pokemon_data):
    """Get Pokemon information from the data."""
    for pokemon in pokemon_data:
        if pokemon["Pokemon"].lower() == pokemon_name.lower():
            moves = pokemon.get("Moves", {})
            counters = pokemon.get("Checks and Counters", [])
            return {
                "raw_count": pokemon.get("Raw Count", 0),
                "viability_ceiling": pokemon.get("Viability Ceiling", 0),
                "moves": moves,
                "counters": counters
            }
    return None 