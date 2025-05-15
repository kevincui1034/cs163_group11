import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import base64
from io import BytesIO
from components.data_loader import load_pokemon_data, get_generation_to_region_mapping, get_stat_columns
from components.visualizations import create_correlation_heatmap, create_total_stats_scatter

# Register page
dash.register_page(__name__, path='/analytical_methods')

# Load and prepare data
df = load_pokemon_data()
df['Region'] = df['Generation'].map(get_generation_to_region_mapping())
stat_cols = get_stat_columns()

# Generate figures
heatmap_fig = create_correlation_heatmap(df, stat_cols)
scatter_fig = create_total_stats_scatter(df, stat_cols)

# --- Elbow Method for Optimal k ---
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[stat_cols])

inertia = []
k_range = range(1, 11)
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)

buffer_elbow = BytesIO()
plt.figure(figsize=(8, 5))
plt.plot(k_range, inertia, marker='o')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia (SSE)')
plt.title('Elbow Method For Optimal k')
plt.grid(True)
plt.tight_layout()
plt.savefig(buffer_elbow, format="png")
plt.close()
buffer_elbow.seek(0)
elbow_plot_base64 = base64.b64encode(buffer_elbow.read()).decode('utf-8')

# --- PCA for Clustering ---
pca = PCA(n_components=2)
pca_components = pca.fit_transform(X_scaled)
df['PCA1'] = pca_components[:, 0]
df['PCA2'] = pca_components[:, 1]

# --- Layout ---
layout = html.Div([
    html.H1('Analytical Methods', style={'textAlign': 'center'}),
    
    html.Div([
        html.P(
            "We examine the relationship between Pokémon stats and their corresponding generation. "
            "Our main hypothesis is that Pokémon become stronger over time due to 'power creep'. "
            "We first mapped each Pokémon's generation to its corresponding region, applied one-hot encoding "
            "to region data, and combined it with the base stats to compute a correlation matrix. "
            "From this, we extracted stat-to-region correlations and visualized them using a heatmap."
        )
    ], style={'marginBottom': '50px'}),
    
    html.Div([
        html.H2("Correlation Heatmap"),
        dcc.Graph(figure=heatmap_fig, className='graph-style')
    ], style={'marginBottom': '70px'}),
    
    html.Div([
        html.Div([
            html.P([
                "Kalos Region Pokémon appear statistically stronger across the board in this dataset, possibly due to design choices in Gen 6 (e.g., Mega Evolutions or smaller Pokédex)."
            ], style={'marginBottom': '15px'}),
            html.P([
                "Kanto Region Pokémon, being older designs, seem to have lower base stats, which could reflect power creep in later generations."
            ], style={'marginBottom': '15px'}),
            html.P([
                "Correlations are mild overall; no value exceeds ±0.2, so while trends are visible, they're not extreme."
            ], style={'marginBottom': '15px'}),
            html.P([
                "Although some generations may be stronger than others, it is not a recurring trend."
            ])
        ]),
    ], style={'marginBottom': '70px'}),
    
    html.Div([
        html.P(
            "Next, we performed K-means clustering and PCA to visualize Pokémon stat groupings. "
            "Pokémon were clustered into four groups based on core battle stats and projected into two dimensions "
            "for easier visualization."
        )
    ], style={'marginBottom': '50px'}),
    
    html.Div([
        html.H2("Elbow Method to Find Optimal k"),
        html.Img(
            src='data:image/png;base64,{}'.format(elbow_plot_base64),
            style={'maxWidth': '100%', 'height': 'auto', 'display': 'block', 'margin': '0 auto'}
        )
    ], style={'marginBottom': '70px'}),
    
    html.Div([
        html.P(
            "To determine the best number of clusters, we applied the Elbow Method. "
            "This technique plots inertia (within-cluster sum of squares) for k = 1 to 10, "
            "helping identify the point where adding more clusters yields diminishing returns."
        )
    ], style={'marginBottom': '50px'}),
    
    html.Div([
        html.H2("Interactive Clustering (K-Means)"),
        dcc.Dropdown(
            id='k-dropdown',
            options=[{'label': f'{k} Clusters', 'value': k} for k in range(2, 11)],
            value=4,
            clearable=False,
            style={'width': '200px', 'margin': '0 auto'}
        ),
        dcc.Graph(id='cluster-graph', className='graph-style')
    ], style={'marginBottom': '70px'}),

    html.Div([
        html.P(
            "We performed K-means clustering with 4 clusters and assigned each Pokémon to one of these clusters. "
            "To visualize the high-dimensional data, we applied PCA to reduce the data to two components "
            "and plotted the results in a scatterplot, colored by cluster. This visualization reveals the "
            "natural groupings of Pokémon based on their stat profiles."
        )
    ], style={'marginBottom': '50px'}),
], style={
    'maxWidth': '1200px',
    'margin': '0 auto',
    'padding': '20px'
})

# --- Callback for clustering ---
@dash.callback(
    Output('cluster-graph', 'figure'),
    Input('k-dropdown', 'value')
)
def update_cluster_plot(k):
    df_copy = df.copy()
    kmeans = KMeans(n_clusters=k, random_state=42)
    df_copy['Cluster'] = kmeans.fit_predict(X_scaled)

    cluster_fig = px.scatter(
        df_copy, x='PCA1', y='PCA2', color='Cluster',
        title=f'K-means Clustering of Pokémon (k={k})',
        labels={'PCA1': 'PCA Component 1', 'PCA2': 'PCA Component 2', 'Cluster': 'Cluster'},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    return cluster_fig
