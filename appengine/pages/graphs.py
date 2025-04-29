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

# Register page
dash.register_page(__name__, path='/graphs')

# --- Data Preparation ---
df = pd.read_csv('https://raw.githubusercontent.com/lgreski/pokemonData/refs/heads/master/Pokemon.csv')

# Mapping generation to region
generation_to_region = {
    1: 'Kanto', 2: 'Johto', 3: 'Hoenn', 4: 'Sinnoh',
    5: 'Unova', 6: 'Kalos', 7: 'Alola', 8: 'Galar', 9: 'Paldea'
}
df['Region'] = df['Generation'].map(generation_to_region)

# Stat columns
stat_cols = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']

# --- Correlation Heatmap (Plotly) ---
region_dummies = pd.get_dummies(df['Region'])
correlation_data = pd.concat([df[stat_cols], region_dummies], axis=1)
correlation_matrix = correlation_data.corr()
region_vs_stats = correlation_matrix.loc[stat_cols, region_dummies.columns]

heatmap_fig = px.imshow(
    region_vs_stats,
    text_auto=True,
    labels=dict(x="Region", y="Stat", color="Correlation"),
    title="Correlation Between Pokémon Stats and Regions"
)

# --- Static Heatmap (Seaborn) ---
numeric_df = df.select_dtypes(include=[np.number])

buffer_heatmap = BytesIO()
plt.figure(figsize=(10, 6))
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Full Numeric Correlation Heatmap")
plt.tight_layout()
plt.savefig(buffer_heatmap, format="png")
plt.close()
buffer_heatmap.seek(0)
static_heatmap_base64 = base64.b64encode(buffer_heatmap.read()).decode('utf-8')

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

# --- Base Stats Scatter Plot ---
df['Total'] = df[stat_cols].sum(axis=1)
mean_total_by_gen = df.groupby('Generation')['Total'].mean().reset_index()

scatter_fig = px.scatter(
    mean_total_by_gen, x='Generation', y='Total',
    trendline="ols", trendline_color_override="red",
    title='Mean Total Base Stats by Pokémon Generation',
    labels={"Total": "Average Total Base Stats"}
)

# --- Layout ---
layout = html.Div([
    html.H1('Graphs Page', style={'textAlign': 'center'}),

    html.Div([
        html.H2("Correlation Heatmap (Interactive)"),
        dcc.Graph(figure=heatmap_fig)
    ], style={'marginBottom': '50px'}),

    html.Div([
        html.H2("Full Numeric Correlation Heatmap (Static)"),
        html.Img(src='data:image/png;base64,{}'.format(static_heatmap_base64),
                 style={'maxWidth': '100%', 'height': 'auto', 'display': 'block', 'margin': '0 auto'})
    ], style={'marginBottom': '50px'}),

    html.Div([
        html.H2("Elbow Method to Find Optimal k"),
        html.Img(src='data:image/png;base64,{}'.format(elbow_plot_base64),
                 style={'maxWidth': '100%', 'height': 'auto', 'display': 'block', 'margin': '0 auto'})
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
        dcc.Graph(id='cluster-graph')
    ], style={'marginBottom': '50px'}),

    html.Div([
        html.H2("Average Base Stats by Generation"),
        dcc.Graph(figure=scatter_fig)
    ])
], style={
    'maxWidth': '1200px',
    'margin': '0 auto',
    'padding': '20px'
})

# --- Callback for interactive clustering ---
@dash.callback(
    Output('cluster-graph', 'figure'),
    Input('k-dropdown', 'value')
)
def update_cluster_plot(k):
    # Create a copy of df
    df_copy = df.copy()

    # Perform clustering
    kmeans = KMeans(n_clusters=k, random_state=42)
    df_copy['Cluster'] = kmeans.fit_predict(X_scaled)

    # Plot
    cluster_fig = px.scatter(
        df_copy, x='PCA1', y='PCA2', color=df_copy['Cluster'].astype(str),
        title=f'K-means Clustering of Pokémon (k={k})',
        labels={'PCA1': 'PCA Component 1', 'PCA2': 'PCA Component 2', 'color': 'Cluster'},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    return cluster_fig
