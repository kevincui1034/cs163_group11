import json
import pandas as pd
import pickle
import os
print("[INFO] Importing sklearn.decomposition.PCA...")
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
import numpy as np

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
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'pokemon_model.pkl')
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

    # Make predictions
    y_pred = clf.predict(X_test)
    
    # Print classification metrics
    print("\n=== Classification Metrics ===")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    print("\nOverall Metrics:")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision (weighted): {precision_score(y_test, y_pred, average='weighted'):.4f}")
    print(f"Recall (weighted): {recall_score(y_test, y_pred, average='weighted'):.4f}")
    print(f"F1 Score (weighted): {f1_score(y_test, y_pred, average='weighted'):.4f}")
    
    # Train a separate model on original features to get feature importance
    X_train_orig, X_test_orig, y_train_orig, y_test_orig = train_test_split(X_scaled, y_data, test_size=0.2, random_state=42)
    clf_orig = RandomForestClassifier(n_estimators=50, random_state=42)
    clf_orig.fit(X_train_orig, y_train_orig)
    
    # Feature importance for original features
    feature_importance = pd.DataFrame({
        'feature': df.columns,
        'importance': clf_orig.feature_importances_
    })
    feature_importance = feature_importance.sort_values('importance', ascending=False)
    
    print("\nTop 10 Most Important Features:")
    print(feature_importance.head(10).to_string(index=False))
    
    # PCA explained variance
    print("\nPCA Explained Variance:")
    print(f"Total explained variance: {sum(pca.explained_variance_ratio_):.4f}")
    for i, ratio in enumerate(pca.explained_variance_ratio_):
        print(f"PC{i+1}: {ratio:.4f}")

    # Class distribution
    class_dist = pd.Series(y_data).value_counts()
    print("\nClass Distribution (Top 10 most common moves):")
    print(class_dist.head(10))

    # Move performance summary
    move_performance = []
    for move in class_dist.index:
        y_true_move = np.array(y_test) == move
        y_pred_move = np.array(y_pred) == move
        if np.any(y_true_move):  # Only calculate metrics if the move appears in test set
            move_performance.append({
                'Move': move,
                'Count': class_dist[move],
                'Precision': precision_score(y_true_move, y_pred_move, zero_division=0),
                'Recall': recall_score(y_true_move, y_pred_move, zero_division=0),
                'F1': f1_score(y_true_move, y_pred_move, zero_division=0)
            })
    
    move_performance_df = pd.DataFrame(move_performance)
    
    print("\nTop 10 Best Performing Moves (by F1 score):")
    print(move_performance_df.sort_values('F1', ascending=False).head(10).to_string(index=False))
    
    print("\nTop 10 Worst Performing Moves (by F1 score):")
    print(move_performance_df.sort_values('F1').head(10).to_string(index=False))

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
        # Add Pokemon 1 features with p1_p1_ prefix
        for k, v in f1.items():
            features[f"p1_{k}"] = v
        # Add Pokemon 2 features with p2_p1_ prefix
        for k, v in f2.items():
            features[f"p2_{k}"] = v

        # Create DataFrame with all expected features
        df_row = pd.DataFrame([features])
        
        # Ensure all expected features exist
        expected_features = [
            'p1_p1_raw_count', 'p1_p1_viability_ceiling',
            'p1_p1_move_1', 'p1_p1_move_2', 'p1_p1_move_3', 'p1_p1_move_4',
            'p1_p1_avg_koed', 'p1_p1_avg_switched',
            'p2_p1_raw_count', 'p2_p1_viability_ceiling',
            'p2_p1_move_1', 'p2_p1_move_2', 'p2_p1_move_3', 'p2_p1_move_4',
            'p2_p1_avg_koed', 'p2_p1_avg_switched'
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

if __name__ == "__main__":
    # Load model and create predictor
    model, scaler, pca, pokemon_data = load_model()
    recommend = build_predictor(model, scaler, pca, pokemon_data)

    # Example usage
    # print(recommend("Kingambit", "Great Tusk"))