import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Register page
dash.register_page(__name__, path='/graphs')

# --- Data Preparation ---
df = pd.read_csv('https://raw.githubusercontent.com/lgreski/pokemonData/refs/heads/master/Pokemon.csv')
generation_to_region = {
    1: 'Kanto', 2: 'Johto', 3: 'Hoenn', 4: 'Sinnoh',
    5: 'Unova', 6: 'Kalos', 7: 'Alola', 8: 'Galar', 9: 'Paldea'
}
df['Region'] = df['Generation'].map(generation_to_region)

# Stat columns
stat_cols = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']

# --- Correlation Heatmap ---
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

# --- PCA for Clustering ---
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[stat_cols])
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
        html.H2("Correlation Heatmap"),
        dcc.Graph(figure=heatmap_fig)
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
    kmeans = KMeans(n_clusters=k, random_state=42)
    df['Cluster'] = kmeans.fit_predict(X_scaled)
    
    cluster_fig = px.scatter(
        df, x='PCA1', y='PCA2', color='Cluster',
        title=f'K-means Clustering of Pokémon (k={k})',
        labels={'PCA1': 'PCA Component 1', 'PCA2': 'PCA Component 2'},
        color_continuous_scale='Set2'
    )
    return cluster_fig
