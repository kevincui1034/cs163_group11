import dash
from dash import html, dcc
import pandas as pd
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from google.cloud import storage
import io

dash.register_page(__name__, path='/major_findings')

def load_data():
    # Initialize GCS client
    storage_client = storage.Client()
    bucket = storage_client.bucket('cs163-group11.appspot.com')
    blob = bucket.blob('gen9ou_full_data.json')
    
    # Download the file content
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

def create_visualizations():
    # Load and process data
    df = load_data()
    
    # Convert teammate combos into vectors
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df['Teammates'])
    
    # Cluster the Pokémon into archetypes
    kmeans = KMeans(n_clusters=4, random_state=42)
    df['Cluster'] = kmeans.fit_predict(X)
    
    # Reduce dimensions for plotting
    pca = PCA(n_components=2)
    components = pca.fit_transform(X.toarray())
    df['PC1'] = components[:, 0]
    df['PC2'] = components[:, 1]
    
    # Calculate average viability for each archetype
    cluster_viability = df.groupby('Cluster')['Viability'].mean().reset_index()
    
    # Create cluster plot
    fig_cluster = px.scatter(
        df,
        x='PC1',
        y='PC2',
        color='Cluster',
        hover_data=['Pokemon', 'Viability'],
        title='Team Archetype Clusters Based on Teammates',
        labels={'PC1': 'Principal Component 1', 'PC2': 'Principal Component 2'}
    )
    
    # Create viability plot
    fig_viability = px.bar(
        cluster_viability,
        x='Cluster',
        y='Viability',
        title='Average Viability by Team Archetype',
        labels={'Cluster': 'Team Archetype', 'Viability': 'Average Viability Score'}
    )
    
    return fig_cluster, fig_viability

# Create the layout
layout = html.Div([
    html.H1("Major Findings", className="text-center mb-4"),
    
    html.Div([
        html.H2("Team Archetype Analysis"),
        html.Div([
            html.P("Our analysis of Pokémon team compositions reveals four distinct team archetypes based on teammate relationships:"),
            html.Ul([
                html.Li([html.Strong("Bulky Offense:"), " Teams that combine defensive walls with powerful attackers"]),
                html.Li([html.Strong("Hyper Offense:"), " Teams focused on speed control and powerful sweepers"]),
                html.Li([html.Strong("Balanced Teams:"), " Teams with a mix of support, pivots, and hazard control"]),
                html.Li([html.Strong("Stall/Fat Balance:"), " Teams built around regeneration cores and defensive tanks"])
            ])
        ], className="mb-4"),
        dcc.Graph(id='cluster-plot', figure=create_visualizations()[0])
    ], className="visualization-section"),
    
    html.Div([
        html.H2("Viability Analysis"),
        html.Div([
            html.P("The visualization below shows the relationship between team archetypes and their average viability scores. This helps identify which team compositions tend to perform better in the current meta.")
        ], className="mb-4"),
        dcc.Graph(id='viability-plot', figure=create_visualizations()[1])
    ], className="visualization-section")
], className="container")