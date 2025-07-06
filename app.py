# app.py
import dash
from dash import dcc, html, Dash
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from flask import Flask
import os

# Initialize the Dash app
server = Flask(__name__)
app = Dash(__name__, server=server)

# Load your dataset
df = pd.read_csv('cleaned_personality_dataset.csv')

# Select only numeric columns for plotting
numeric_cols = df.select_dtypes(include='number').columns.tolist()

# Define your layout
app.layout = html.Div([
    html.H1('Personality Traits Data Dashboard'),
    dcc.Dropdown(
        id='selector',
        options=[{'label': col, 'value': col} for col in numeric_cols],
        value=numeric_cols[0],
        style={'width': '50%'}
    ),
    dcc.Graph(id='graph')
])

# Define your callback
@app.callback(
    Output('graph', 'figure'),
    [Input('selector', 'value')]
)
def update_graph(selected_value):
    fig = px.histogram(df, x=selected_value, color='Personality', barmode='overlay', nbins=20,
                       title=f'Distribution of {selected_value} by Personality')
    return fig

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run(debug=False, host="0.0.0.0", port=port)

