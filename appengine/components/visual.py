# 📌 STEP 1: Install dependencies (if needed)
# Run this in your terminal or uncomment for Jupyter: !pip install scikit-learn matplotlib pandas

# 📌 STEP 2: Import libraries
import pandas as pd
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np

# 📌 STEP 3: Load and parse JSON data
file_path = './data/gen9ou_full_data.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# 📌 STEP 4: Create a DataFrame with teammates and viability
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

df = pd.DataFrame(rows)

# 📌 STEP 5: Convert teammate combos into vectors
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['Teammates'])

# 📌 STEP 6: Cluster the Pokémon into archetypes
kmeans = KMeans(n_clusters=4, random_state=42)
df['Cluster'] = kmeans.fit_predict(X)

# 📌 STEP 7: Reduce dimensions for plotting
pca = PCA(n_components=2)
components = pca.fit_transform(X.toarray())
df['PC1'] = components[:, 0]
df['PC2'] = components[:, 1]

# 📌 STEP 8: Calculate average viability for each archetype
cluster_viability = df.groupby('Cluster')['Viability'].mean().reset_index()

# 📌 STEP 9: Plot the clusters
plt.figure(figsize=(10, 6))
colors = plt.cm.viridis(np.linspace(0, 1, 4))
scatter = plt.scatter(df['PC1'], df['PC2'], c=df['Cluster'], cmap='viridis', alpha=0.7)
plt.colorbar(scatter, label='Cluster')
for i, row in cluster_viability.iterrows():
    plt.text(df[df['Cluster'] == row['Cluster']]['PC1'].mean(),
             df[df['Cluster'] == row['Cluster']]['PC2'].mean(),
             f"Avg V: {row['Viability']:.1f}", fontsize=12, weight='bold')

# Add custom legend with consistent colors
legend_labels = {
    0: "Bulky Offense",
    1: "Hyper Offense",
    2: "Balanced",
    3: "Stall / Fat Balance"
}
handles = [plt.Line2D([0], [0], marker='o', color='w', label=f"Cluster {i}: {label}",
                      markerfacecolor=colors[i], markersize=10)
           for i, label in legend_labels.items()]
plt.legend(handles=handles, title="Team Archetypes", loc='upper right')

plt.title('Team Archetype Clusters Based on Teammates')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.grid(True)
plt.tight_layout()
plt.show()

# 📌 STEP 10: Print legend for what the clusters may represent
print("\nCluster Legend (based on teammate composition):")
print("Cluster 0 - Likely Bulky Offense: Mix of walls + hard hitters")
print("Cluster 1 - Hyper Offense: Speed boosters, glass cannons, sweepers")
print("Cluster 2 - Balanced Teams: Status support, pivots, hazard control")
print("Cluster 3 - Stall or Fat Balance: Regen cores, setup blockers, tanks")

# 📌 Optional: Display table of Pokémon and their clusters
print(df[['Pokemon', 'Cluster', 'Viability']].sort_values(by='Cluster').head(20))