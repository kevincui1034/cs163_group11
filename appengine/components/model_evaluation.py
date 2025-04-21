import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import pandas as pd
import numpy as np
from pokemon_move_recommender import train_model, is_threatened

def evaluate_model():
    # Load data and train model
    with open("./data/gen9ou_full_data.json", "r") as f:
        pokemon_data = json.load(f)

    clf, scaler, pca, df, data = train_model(pokemon_data)

    # Get predictions for all test data
    X_scaled = scaler.transform(df)
    X_pca = pca.transform(X_scaled)
    y_pred = clf.predict(X_pca)

    # Get true labels
    y_true = []
    for p1 in pokemon_data:
        for p2 in pokemon_data:
            if p1["Pokemon"] == p2["Pokemon"]:
                continue

            p1_moves = list(p1.get("Moves", {}).keys())
            best_move = sorted(p1["Moves"].items(), key=lambda x: x[1], reverse=True)[0][0] if p1_moves else "SWITCH"
            
            label = "SWITCH" if is_threatened(p1, p2["Pokemon"]) else best_move
            if label != "SWITCH" and label not in p1_moves:
                label = "SWITCH"
            
            y_true.append(label)

    # Calculate metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='weighted')
    recall = recall_score(y_true, y_pred, average='weighted')
    f1 = f1_score(y_true, y_pred, average='weighted')
    
    # Calculate error rate
    error_rate = 1 - accuracy

    # Get confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    unique_labels = sorted(set(y_true + list(y_pred)))
    
    # Print results
    print("\nModel Evaluation Metrics:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Error Rate: {error_rate:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    
    print("\nConfusion Matrix:")
    cm_df = pd.DataFrame(cm, index=unique_labels, columns=unique_labels)
    print(cm_df)

if __name__ == "__main__":
    evaluate_model() 