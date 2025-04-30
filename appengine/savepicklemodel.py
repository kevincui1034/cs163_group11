import os
import json
import pickle
from components.pokemon_move_recommender import train_model

# Load your data
with open("components/data/gen9ou_full_data.json", "r") as f:
    pokemon_data = json.load(f)

# Train model
clf, scaler, pca, df, data = train_model(pokemon_data)

# ✅ Make sure the folder exists before saving
os.makedirs("models", exist_ok=True)

# Save the model
with open("models/pokemon_model.pkl", "wb") as f:
    pickle.dump((clf, scaler, pca, df, data), f)

print("✅ Model saved successfully to models/pokemon_model.pkl")
