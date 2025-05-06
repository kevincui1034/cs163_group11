import json
import pandas as pd
import pickle
import os
print("[INFO] Importing sklearn.decomposition.PCA...")
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# --- Feature Extraction ---
def extract_features_from_full(p):
    """Extract features from Pokemon data with consistent feature names."""
    features = {}
    # Base stats
    features["p1_raw_count"] = p.get("Raw Count", 0)
    features["p1_viability_ceiling"] = p.get("Viability Ceiling", 0)

    # Move features - ensure all 4 move slots exist
    moves = p.get("Moves", {})
    if isinstance(moves, str):
        # If moves is a string (space-separated list), convert to dict
        moves = {move: 1.0 for move in moves.split()}
    sorted_moves = sorted(moves.items(), key=lambda x: x[1], reverse=True)[:4]
    for i in range(4):  # Always create 4 move slots
        if i < len(sorted_moves):
            features[f"p1_move_{i+1}"] = sorted_moves[i][1]
        else:
            features[f"p1_move_{i+1}"] = 0.0

    # Counter features
    counters = p.get("Checks and Counters", [])
    if isinstance(counters, str):
        # If counters is a string, convert to empty list
        counters = []
    if counters:
        avg_ko = sum(c.get("KOed", 0) for c in counters) / len(counters)
        avg_sw = sum(c.get("Switched Out", 0) for c in counters) / len(counters)
    else:
        avg_ko = avg_sw = 0.0
    features["p1_avg_koed"] = avg_ko
    features["p1_avg_switched"] = avg_sw

    return features

# --- Threat Logic ---
def is_threatened(p1, p2_name):
    counters = p1.get("Checks and Counters", [])
    if isinstance(counters, str):
        counters = []
    for counter in counters:
        if p2_name.lower() in counter.get("Name", "").lower():
            return counter.get("KOed", 0) > 25 and counter.get("Switched Out", 0) > 40
    return False

# --- Model Loading ---
def load_model():
    """Load the trained model from local file."""
    model_path = os.path.join('components', 'models', 'pokemon_model.pkl')
    try:
        print(f"Attempting to load model from: {os.path.abspath(model_path)}")
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
            print(f"Successfully loaded model data")
            print(f"Model data type: {type(model_data)}")
            if isinstance(model_data, tuple):
                print(f"Number of elements in tuple: {len(model_data)}")
                for i, item in enumerate(model_data):
                    print(f"Element {i} type: {type(item)}")
            return model_data
    except FileNotFoundError:
        print(f"Model file not found at: {os.path.abspath(model_path)}")
        raise FileNotFoundError(f"Model file not found at {model_path}. Please ensure the model file exists.")
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        print(f"Error type: {type(e)}")
        raise Exception(f"Error loading model: {str(e)}")

# --- Model Training ---
def train_model(pokemon_data):
    X_data = []
    y_data = []

    for p1 in pokemon_data:
        for p2 in pokemon_data:
            if p1["Pokemon"] == p2["Pokemon"]:
                continue

            f1 = extract_features_from_full(p1)
            f2 = extract_features_from_full(p2)
            row = {f"p1_{k}": v for k, v in f1.items()}
            row.update({f"p2_{k}": v for k, v in f2.items()})

            p1_moves = list(p1.get("Moves", {}).keys())
            best_move = sorted(p1["Moves"].items(), key=lambda x: x[1], reverse=True)[0][0] if p1_moves else "SWITCH"

            label = "SWITCH" if is_threatened(p1, p2["Pokemon"]) else best_move
            if label != "SWITCH" and label not in p1_moves:
                label = "SWITCH"

            X_data.append(row)
            y_data.append(label)

    df = pd.DataFrame(X_data).fillna(0)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df)

    pca = PCA(n_components=5)
    X_pca = pca.fit_transform(X_scaled)

    X_train, X_test, y_train, y_test = train_test_split(X_pca, y_data, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X_train, y_train)

    return clf, scaler, pca, df, pokemon_data

# --- Prediction Function ---
def build_predictor(model, scaler, pca, pokemon_data):
    name_to_features = {p["Pokemon"]: extract_features_from_full(p) for p in pokemon_data}

    def recommend_move(pokemon_1_name, pokemon_2_name):
        if pokemon_1_name not in name_to_features or pokemon_2_name not in name_to_features:
            return f"Error: One of the Pokémon ('{pokemon_1_name}', '{pokemon_2_name}') not found."

        # Get features for both Pokemon
        f1 = name_to_features[pokemon_1_name]
        f2 = name_to_features[pokemon_2_name]

        # Create feature dictionary with consistent naming
        features = {}
        # Add Pokemon 1 features
        for k, v in f1.items():
            features[k] = v
        # Add Pokemon 2 features with p2_ prefix
        for k, v in f2.items():
            features[k.replace('p1_', 'p2_')] = v

        # Create DataFrame with all expected features
        df_row = pd.DataFrame([features])
        
        # Ensure all expected features exist
        expected_features = [
            'p1_raw_count', 'p1_viability_ceiling',
            'p1_move_1', 'p1_move_2', 'p1_move_3', 'p1_move_4',
            'p1_avg_koed', 'p1_avg_switched',
            'p2_raw_count', 'p2_viability_ceiling',
            'p2_move_1', 'p2_move_2', 'p2_move_3', 'p2_move_4',
            'p2_avg_koed', 'p2_avg_switched'
        ]
        
        # Fill missing features with 0
        for feature in expected_features:
            if feature not in df_row.columns:
                df_row[feature] = 0

        # Ensure columns are in the same order as training data
        df_row = df_row[expected_features]

        # Transform data
        scaled = scaler.transform(df_row)
        pca_input = pca.transform(scaled)

        # Make prediction
        prediction = model.predict(pca_input)[0]

        # Validate prediction
        p1_data = next((p for p in pokemon_data if p["Pokemon"] == pokemon_1_name), None)
        if p1_data:
            moves = p1_data.get("Moves", {})
            if isinstance(moves, str):
                moves = {move: 1.0 for move in moves.split()}
            if prediction not in moves:
                if moves:
                    fallback = sorted(moves.items(), key=lambda x: x[1], reverse=True)[0][0]
                    return f"Recommended move: {fallback}"
                else:
                    return "Recommended action: SWITCH"

        return f"Recommended move: {prediction}"

    return recommend_move

if __name__ == "__main__":
    # Load model and create predictor
    model, scaler, pca, pokemon_data = load_model()
    recommend = build_predictor(model, scaler, pca, pokemon_data)

    # Example usage
    # print(recommend("Kingambit", "Great Tusk"))