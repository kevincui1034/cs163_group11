import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def create_correlation_heatmap(df, stat_cols):
    region_dummies = pd.get_dummies(df['Region'])
    correlation_data = pd.concat([df[stat_cols], region_dummies], axis=1)
    correlation_matrix = correlation_data.corr()
    region_vs_stats = correlation_matrix.loc[stat_cols, region_dummies.columns]

    return px.imshow(
        region_vs_stats,
        text_auto=True,
        labels=dict(x="Region", y="Stat", color="Correlation"),
        title="Correlation Between Pokémon Stats and Regions"
    )

def create_stats_correlation_heatmap(df, stat_cols):
    # Calculate correlation matrix for base stats
    correlation_matrix = df[stat_cols].corr()
    
    # Create heatmap
    fig = px.imshow(
        correlation_matrix,
        text_auto='.2f',
        color_continuous_scale='RdBu',
        aspect='auto',
        title='Correlation Between Base Stats'
    )
    
    # Update layout for better readability
    fig.update_layout(
        xaxis_title='Base Stat',
        yaxis_title='Base Stat',
        coloraxis_colorbar=dict(
            title='Correlation'
        )
    )
    
    # Update hover template to show correlation value
    fig.update_traces(
        hovertemplate='<b>%{y}</b> vs <b>%{x}</b><br>Correlation: %{z:.2f}<extra></extra>'
    )
    
    return fig

def create_total_stats_scatter(df, stat_cols):
    df['Total'] = df[stat_cols].sum(axis=1)
    mean_total_by_gen = df.groupby('Generation')['Total'].mean().reset_index()

    return px.scatter(
        mean_total_by_gen, x='Generation', y='Total',
        trendline="ols", trendline_color_override="red",
        title='Mean Total Base Stats by Pokémon Generation',
        labels={"Total": "Average Total Base Stats"}
    )

def create_total_stats_boxplot(df, stat_cols):
    df['Total'] = df[stat_cols].sum(axis=1)
    
    fig = px.box(
        df,
        x='Generation',
        y='Total',
        title='Distribution of Total Base Stats by Generation',
        labels={
            'Generation': 'Pokémon Generation',
            'Total': 'Total Base Stats'
        },
        color='Generation',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    # Update layout for better readability
    fig.update_layout(
        showlegend=False,
        xaxis=dict(
            tickmode='linear',
            tick0=1,
            dtick=1
        ),
        yaxis=dict(
            range=[df['Total'].min() - 50, df['Total'].max() + 50]
        )
    )
    
    return fig

def create_team_archetype_visuals(df):
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

    # Define cluster labels and colors
    cluster_labels = {
        0: "Bulky Offense",
        1: "Hyper Offense",
        2: "Balanced Teams",
        3: "Stall/Fat Balance"
    }
    cluster_colors = {
        0: "#1f77b4",  # blue
        1: "#ff7f0e",  # orange
        2: "#2ca02c",  # green
        3: "#d62728"   # red
    }

    # Map cluster numbers to labels
    df['Cluster_Label'] = df['Cluster'].map(cluster_labels)

    # Calculate average viability for each cluster
    cluster_viability = df.groupby('Cluster_Label')['Viability'].mean().reset_index()

    # Create scatter plot with text labels
    fig = go.Figure()
    
    # Add scatter points for each cluster
    for cluster_num, label in cluster_labels.items():
        cluster_data = df[df['Cluster'] == cluster_num]
        avg_viability = cluster_viability[cluster_viability['Cluster_Label'] == label]['Viability'].iloc[0]
        fig.add_trace(go.Scatter(
            x=cluster_data['PC1'],
            y=cluster_data['PC2'],
            mode='markers',
            name=f"{label} (Avg Viability: {avg_viability:.2f})",
            marker=dict(
                size=10,
                color=cluster_colors[cluster_num]
            ),
            hovertemplate="<b>%{text}</b><extra></extra>",
            text=cluster_data['Pokemon']
        ))

    # Update layout
    fig.update_layout(
        title='Team Archetype Clusters Based on Teammates',
        xaxis_title='Principal Component 1',
        yaxis_title='Principal Component 2',
        showlegend=True,
        legend=dict(
            title="Team Archetype",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.05
        )
    )

    # Viability bar plot
    fig_viability = px.bar(
        cluster_viability, 
        x='Cluster_Label', 
        y='Viability',
        title='Average Viability by Team Archetype',
        labels={
            'Cluster_Label': 'Team Archetype', 
            'Viability': 'Average Viability Score'
        },
        color='Cluster_Label',
        color_discrete_map=cluster_colors
    )

    return fig, fig_viability

def create_move_usage_graph(moves_data, pokemon_name):
    """Create a bar graph showing move usage percentages."""
    import plotly.express as px
    import pandas as pd
    
    moves_df = pd.DataFrame(list(moves_data.items()), columns=['Move', 'Usage %'])
    return px.bar(moves_df, x='Move', y='Usage %',
                 title=f'{pokemon_name} Move Usage',
                 color='Usage %',
                 color_continuous_scale='Viridis')

def create_counter_graph(counters_data, pokemon_name):
    """Create a bar graph showing counter effectiveness."""
    import plotly.graph_objects as go
    import pandas as pd
    
    counters_df = pd.DataFrame(counters_data)
    if not counters_df.empty:
        fig = go.Figure(data=[
            go.Bar(name='KO %', x=counters_df['Name'], y=counters_df['KOed']),
            go.Bar(name='Switch %', x=counters_df['Name'], y=counters_df['Switched Out'])
        ])
        fig.update_layout(
            title=f'{pokemon_name} Counters',
            barmode='group',
            xaxis_title='Counter Pokemon',
            yaxis_title='Percentage'
        )
    else:
        fig = go.Figure()
        fig.add_annotation(text="No counter data available",
                         xref="paper", yref="paper",
                         x=0.5, y=0.5, showarrow=False)
    return fig 