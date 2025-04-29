import dash
from dash import html

dash.register_page(__name__, path='/data')

layout = html.Div([
    html.Div([
        html.H1('Data Page', style={'textAlign': 'center'}),
        html.Div('Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.', 
                style={'textAlign': 'center', 'maxWidth': '800px', 'margin': '0 auto'}),
    ], style={
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center',
        'minHeight': '80vh',
        'padding': '20px',
        'maxWidth': '1200px',
        'margin': '0 auto'
    })
])