import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import numpy as np
# Load JSON data
with open("gen9ou_full_data.json") as f:
    data = json.load(f)

# Extract features + counter with highest KOed
def build_training_row(pokemon):
    try:
        top_counter = max(pokemon['Checks and Counters'], key=lambda x: x["KOed"])
        return {
            "Pokemon": pokemon["Pokemon"],
            "Raw Count": pokemon["Raw Count"],
            "Viability Ceiling": pokemon["Viability Ceiling"],
            "Top Ability": max(pokemon["Abilities"], key=pokemon["Abilities"].get),
            "Top Item": max(pokemon["Items"], key=pokemon["Items"].get),
            "Top Tera Type": max(pokemon["Tera Types"], key=pokemon["Tera Types"].get),
            "Best Counter": top_counter["Name"].split()[0]  # Extract just Pokémon name
        }
    except:
        return None

# Build dataset
dataset = [build_training_row(p) for p in data if build_training_row(p)]
df = pd.DataFrame(dataset)

# Prepare X and y
y = df["Best Counter"]
X = df.drop(["Pokemon", "Best Counter"], axis=1)

# One-hot encode features
X_encoded = pd.get_dummies(X)

# Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y_encoded, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
present_labels = sorted(set(y_test) | set(y_pred))
present_classes = le.inverse_transform(present_labels)

# Report
print(classification_report(y_test, y_pred, target_names=present_classes))

proba = model.predict_proba(X_test)
top_3_preds = np.argsort(proba, axis=1)[:, -3:]  # top 3 indexes

# Check if true label is in top 3
hits = [y_test[i] in top_3_preds[i] for i in range(len(y_test))]

# Top-3 Accuracy
top3_acc = sum(hits) / len(hits)
print(f"Top-3 Accuracy: {top3_acc:.2f}")