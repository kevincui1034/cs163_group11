import json
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# --- Feature Extraction ---
def extract_features_from_full(p):
    features = {}
    features["raw_count"] = p.get("Raw Count", 0)
    features["viability_ceiling"] = p.get("Viability Ceiling", 0)

    moves = p.get("Moves", {})
    sorted_moves = sorted(moves.items(), key=lambda x: x[1], reverse=True)[:4]
    for i, (move, pct) in enumerate(sorted_moves):
        features[f"move_{i+1}"] = pct

    counters = p.get("Checks and Counters", [])
    if counters:
        avg_ko = sum(c["KOed"] for c in counters) / len(counters)
        avg_sw = sum(c["Switched Out"] for c in counters) / len(counters)
    else:
        avg_ko = avg_sw = 0.0
    features["avg_koed"] = avg_ko
    features["avg_switched"] = avg_sw

    return features

# --- Threat Logic ---
def is_threatened(p1, p2_name):
    for counter in p1.get("Checks and Counters", []):
        if p2_name.lower() in counter["Name"].lower():
            return counter["KOed"] > 25 and counter["Switched Out"] > 40
    return False

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

        f1 = name_to_features[pokemon_1_name]
        f2 = name_to_features[pokemon_2_name]
        row = {f"p1_{k}": v for k, v in f1.items()}
        row.update({f"p2_{k}": v for k, v in f2.items()})

        df_row = pd.DataFrame([row]).fillna(0)
        scaled = scaler.transform(df_row)
        pca_input = pca.transform(scaled)

        prediction = model.predict(pca_input)[0]

        # Validate prediction
        move_dict = next((p["Moves"] for p in pokemon_data if p["Pokemon"] == pokemon_1_name), {})
        if prediction not in move_dict:
            if move_dict:
                fallback = sorted(move_dict.items(), key=lambda x: x[1], reverse=True)[0][0]
                return f"Recommended move: {fallback}"
            else:
                return "Recommended action: SWITCH"

        return f"Recommended move: {prediction}"

    return recommend_move

if __name__ == "__main__":
    with open("gen9ou_full_data.json", "r") as f:
        pokemon_data = json.load(f)

    clf, scaler, pca, df, data = train_model(pokemon_data)

    recommend = build_predictor(clf, scaler, pca, data)

    # Code to try prediction
    # print(recommend("Kingambit", "Great Tusk"))