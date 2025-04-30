import dash
from dash import html, dcc, Input, Output
import pandas as pd
import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import plotly.express as px
from google.cloud import storage
import io

# Register page
dash.register_page(__name__, path='/major_findings')

# --- Load Gen9OU Data from GCS ---
def load_gen9ou_data():
    storage_client = storage.Client()
    bucket = storage_client.bucket('cs163-group11.appspot.com')
    blob = bucket.blob('gen9ou_full_data.json')
    content = blob.download_as_string()
    data = json.loads(content)
    
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
    return pd.DataFrame(rows)

# --- Load Pokémon Stats Data ---
def load_pokemon_stats():
    storage_client2 = storage.Client()
    bucket2 = storage_client2.bucket('cs163-group11.appspot.com')
    blob2 = bucket2.blob('Pokemon.csv')
    content2 = blob2.download_as_string()
    df = pd.read_csv(io.BytesIO(content2))
    
    generation_to_region = {
        1: 'Kanto', 2: 'Johto', 3: 'Hoenn', 4: 'Sinnoh',
        5: 'Unova', 6: 'Kalos', 7: 'Alola', 8: 'Galar', 9: 'Paldea'
    }
    df['Region'] = df['Generation'].map(generation_to_region)
    return df

# --- Create Visualizations for Major Findings ---
def create_major_findings_visuals():
    df = load_gen9ou_data()

    # Text vectorization on teammate data
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df['Teammates'])

    # KMeans clustering
    kmeans = KMeans(n_clusters=4, random_state=42)
    df['Cluster'] = kmeans.fit_predict(X)

    # PCA for dimensionality reduction
    pca = PCA(n_components=2)
    components = pca.fit_transform(X.toarray())
    df['PC1'] = components[:, 0]
    df['PC2'] = components[:, 1]

    # Grouped viability scores
    cluster_viability = df.groupby('Cluster')['Viability'].mean().reset_index()

    # Cluster scatter plot
    fig_cluster = px.scatter(
        df, x='PC1', y='PC2', color='Cluster',
        hover_data=['Pokemon', 'Viability'],
        title='Team Archetype Clusters Based on Teammates',
        labels={'PC1': 'Principal Component 1', 'PC2': 'Principal Component 2'}
    )

    # Viability bar plot
    fig_viability = px.bar(
        cluster_viability, x='Cluster', y='Viability',
        title='Average Viability by Team Archetype',
        labels={'Cluster': 'Team Archetype', 'Viability': 'Average Viability Score'}
    )

    return fig_cluster, fig_viability

# --- Create Additional Graphs (Correlation & Stats) ---
def create_graphs_visuals():
    df = load_pokemon_stats()
    stat_cols = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']

    # Correlation heatmap
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

    # PCA for base stats
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[stat_cols])
    pca = PCA(n_components=2)
    pca_components = pca.fit_transform(X_scaled)
    df['PCA1'] = pca_components[:, 0]
    df['PCA2'] = pca_components[:, 1]

    # Total base stats scatter
    df['Total'] = df[stat_cols].sum(axis=1)
    mean_total_by_gen = df.groupby('Generation')['Total'].mean().reset_index()

    scatter_fig = px.scatter(
        mean_total_by_gen, x='Generation', y='Total',
        trendline="ols", trendline_color_override="red",
        title='Mean Total Base Stats by Pokémon Generation',
        labels={"Total": "Average Total Base Stats"}
    )

    return heatmap_fig, scatter_fig

# --- Generate Figures ---
fig_cluster, fig_viability = create_major_findings_visuals()
heatmap_fig, scatter_fig = create_graphs_visuals()

# --- Layout ---
layout = html.Div([
    html.H1("Major Findings", style={'textAlign': 'center', 'marginBottom': '30px'}),

    html.Div([
        html.H2("Team Archetype Analysis"),
        html.P("Our analysis of Pokémon team compositions reveals four distinct team archetypes based on teammate relationships:"),
        html.Ul([
            html.Li([html.Strong("Bulky Offense:"), " Teams combining defensive walls with powerful attackers."]),
            html.Li([html.Strong("Hyper Offense:"), " Teams focused on speed control and powerful sweepers."]),
            html.Li([html.Strong("Balanced Teams:"), " Teams with a mix of support, pivots, and hazard control."]),
            html.Li([html.Strong("Stall/Fat Balance:"), " Teams built around regeneration cores and defensive tanks."])
        ]),
        dcc.Graph(figure=fig_cluster, className='graph-style')
    ], style={'marginBottom': '70px'}),

    html.Div([
        html.H2("Viability Analysis"),
        html.P("The visualization below shows the relationship between team archetypes and their average viability scores."),
        dcc.Graph(figure=fig_viability, className='graph-style')
    ], style={'marginBottom': '70px'}),

    html.Hr(),

    html.Div([
        html.H1('Additional Graphs', style={'textAlign': 'center', 'marginTop': '50px'}),
        
        html.Div([
            html.H2("Correlation Heatmap Between Stats"),
            dcc.Graph(figure=heatmap_fig, className='graph-style')
        ], style={'marginBottom': '70px'}),

        html.Div([
            html.H2("Average Base Stats by Generation"),
            dcc.Graph(figure=scatter_fig, className='graph-style')
        ])
    ], style={
        'maxWidth': '1200px',
        'margin': '0 auto',
        'padding': '20px'
    })
])
