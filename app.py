import dash
from dash import dcc, html, Input, Output, State, dash_table
import plotly.express as px
import pandas as pd
import base64
import io
from flask import Flask
import os

# Initialize Flask server and Dash app
server = Flask(__name__)
app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True)

# App layout
app.layout = html.Div(children=[
    html.H1(children='Data Visualisation Dashboard'),

    html.Hr(),

    html.Div('Upload a dataset:'),

    dcc.Upload(
        id='file-upload',
        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
            'background-color': '#f0f0f0'
        },
        multiple=False,
        accept='.csv,.xlsx,.xls,.json'
    ),

    dcc.Store(id='dataset-store', storage_type='session'),

    html.Br(),
    html.H3('Preview of Uploaded Data:'),
    dash_table.DataTable(
        id='data-preview',
        columns=[],
        data=[],
        style_table={'overflowX': 'auto'}
    ),

    html.Br(),
    html.Div('Select Column to Visualize:'),
    dcc.Dropdown(id='selector', options=[], value=None, style={'width': '50%'}),
    dcc.Graph(id='graph'),

    html.Br(),
    html.Button('Download Stored Data', id='download-button', n_clicks=0),
    dcc.Download(id='data-download')
])

# Helper to decode uploaded files
def load_data(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if filename.endswith('.csv'):
            return pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif filename.endswith(('.xls', '.xlsx')):
            return pd.read_excel(io.BytesIO(decoded))
        elif filename.endswith('.json'):
            import json
            return pd.DataFrame(json.loads(decoded.decode('utf-8')))
        else:
            return pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    except Exception as e:
        print(f"Error loading file: {e}")
        return pd.DataFrame()

# Callback to update data store and table
@app.callback(
    [Output('dataset-store', 'data'),
     Output('data-preview', 'data'),
     Output('data-preview', 'columns'),
     Output('selector', 'options'),
     Output('selector', 'value')],
    Input('file-upload', 'contents'),
    State('file-upload', 'filename'),
    prevent_initial_call=True
)
def update_output(contents, filename):
    if contents is not None:
        df = load_data(contents, filename)
        data = df.to_dict('records')
        columns = [{'name': col, 'id': col} for col in df.columns]
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        selector_options = [{'label': col, 'value': col} for col in numeric_cols]
        selector_value = numeric_cols[0] if numeric_cols else None
        return data, data, columns, selector_options, selector_value
    return None, [], [], [], None

# Callback to update graph
@app.callback(
    Output('graph', 'figure'),
    Input('selector', 'value'),
    State('dataset-store', 'data'),
    prevent_initial_call=True
)
def update_graph(selected_value, stored_data):
    if stored_data is not None and selected_value:
        df = pd.DataFrame(stored_data)
        if 'Personality' in df.columns:
            fig = px.histogram(df, x=selected_value, color='Personality', barmode='overlay', nbins=20,
                               title=f'Distribution of {selected_value} by Personality')
        else:
            fig = px.histogram(df, x=selected_value, nbins=20,
                               title=f'Distribution of {selected_value}')
        return fig
    return {}

# Callback for download
@app.callback(
    Output('data-download', 'data'),
    Input('download-button', 'n_clicks'),
    State('dataset-store', 'data'),
    prevent_initial_call=True
)
def download_data(n_clicks, data):
    if data:
        df = pd.DataFrame(data)
        return dict(content=df.to_csv(index=False), filename='stored_data.csv')
    return None

# Run server
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run(debug=False, host="0.0.0.0", port=port)
