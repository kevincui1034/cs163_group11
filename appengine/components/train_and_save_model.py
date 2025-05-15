import json
import pickle
import os
from pokemon_move_recommender import train_model

def load_pokemon_data():
    """Load Pokemon data from the JSON file."""
    data_path = os.path.join('appengine', 'components', 'data', 'gen9ou_full_data.json')
    try:
        with open(data_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Pokemon data file not found at {data_path}")
        raise
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {data_path}")
        raise

def save_model(model_data):
    """Save the trained model and its components to a pickle file."""
    model_path = os.path.join('appengine', 'components', 'models', 'pokemon_model.pkl')
    try:
        with open(model_path, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"Model successfully saved to {model_path}")
    except Exception as e:
        print(f"Error saving model: {str(e)}")
        raise

def main():
    print("Loading Pokemon data...")
    pokemon_data = load_pokemon_data()
    
    print("Training model...")
    model, scaler, pca, df, pokemon_data = train_model(pokemon_data)
    
    print("Saving model...")
    model_data = (model, scaler, pca, df, pokemon_data)
    save_model(model_data)
    
    print("Done!")

if __name__ == "__main__":
    main() 