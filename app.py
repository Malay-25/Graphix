import dash
from dash import dcc, html, Input, Output, State, dash_table
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import base64
import io
from flask import Flask
import os
import dash_bootstrap_components as dbc
import numpy as np

# Flask server + Dash app
server = Flask(__name__)
app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP])

# Login layout
login_layout = dbc.Container([
    html.H1('Graphix Dashboard Login'),
    html.Br(),
    dbc.Input(type='text', placeholder='Username', id='username'),
    html.Br(),
    dbc.Input(type='password', placeholder='Password', id='password'),
    html.Br(),
    dbc.Button('Login', id='login-button', color='primary'),
    html.Div(id='auth-output')
], className='col-md-4 offset-md-4', style={"marginTop": "100px"})

# Dashboard layout
dashboard_layout = dbc.Container([
    html.H1('Welcome to Graphix', className='header-text'),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            html.H3('Upload a dataset:'),
            dcc.Upload(
                id='file-upload',
                children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
                style={
                    'width': '100%', 'height': '60px', 'lineHeight': '60px',
                    'borderWidth': '1px', 'borderStyle': 'dashed', 'borderColor' : '#4cc9f0',
                    'borderRadius': '5px', 'textAlign': 'center',
                    'margin': '10px', 'backgroundColor': 'aliceblue'
                },
                multiple=False,
                accept='.csv,.xlsx,.xls,.json'
            ),
            dcc.Store(id='dataset-store', storage_type='session'),
        ], width=12)
    ]),

    html.H3('Filter and Sort Data:'),

    dbc.Row([
        dbc.Col([
            html.Label('Select column to sort:'),
            dcc.Dropdown(id='sort-column', options=[], value=None, 
                         style={
                             'width': '100%'})
        ], md=4, xs=12),
        dbc.Col([
            html.Label('Sort Order:'),
            dcc.Dropdown(
                id='sort-order',
                options=[
                    {'label': 'Ascending', 'value': 'asc'},
                    {'label': 'Descending', 'value': 'desc'}
                ],
                value='asc',
                style={'width': '100%'}
            )
        ], md=4, xs=12),
        dbc.Col([
            html.Label('Select column to filter:'),
            dcc.Dropdown(id='filter-column', options=[], value=None, style={'width': '100%'})
        ], md=4, xs=12),
    ], className='mb-3'),

    dbc.Row([
        dbc.Col([
            html.Label(id='slider-label', children='Filter by selected column:'),
            dcc.Slider(
                id='filter-slider',
                min=0, max=100, step=10, value=100,
                tooltip={"placement": "bottom", "always_visible": True},
                marks={}
            ),
        ], width=12),
    ]),

    html.Br(),
    html.H3('Preview of Uploaded Data:'),

    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                id='data-preview',
                columns=[], data=[],
                style_table={'overflowX': 'auto', 'width': '100%'},
                style_cell={'textAlign': 'left', 'minWidth': '100px', 'whiteSpace': 'normal'}
            ),
        ], width=12)
    ]),

    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Div('Select Column to Visualize:'),
            dcc.Dropdown(id='selector', options=[], value=None, style={'width': '100%'}),
        ], md=4, xs=12),
        dbc.Col([
            html.Div('Group By (Optional):'),
            dcc.Dropdown(id='groupby', options=[], value=None, style={'width': '100%'})
        ], md=4, xs=12),
        dbc.Col([
            html.Div('Plot Type:'),
            dcc.Dropdown(
                id='plot-type',
                options=[
                    {'label': 'Histogram', 'value': 'histogram'},
                    {'label': 'Bar Chart', 'value': 'bar'},
                    {'label': 'Line Chart', 'value': 'line'},
                    {'label': 'Box Plot', 'value': 'box'},
                    {'label': 'Scatter Plot', 'value': 'scatter'}
                ],
                value='histogram',
                style={'width': '100%'}
            )
        ], md=4, xs=12),
    ]),

    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='graph',
                config={'responsive': True},
                style={'width': '100%', 'height': '100%'}
            )
        ], width=12),
    ]),

    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Button('Download Stored Data', id='download-button', n_clicks=0),
            dcc.Download(id='data-download')
        ], width=12)
    ])
], fluid=True, className='p-4')


# Main layout with login toggle
app.layout = html.Div([
    html.Div(login_layout, id='login-page'),
    html.Div(dashboard_layout, id='main-content', style={'display': 'none'})
])

# Callback: login authentication
@app.callback(
    Output('main-content', 'style'),
    Output('login-page', 'style'),
    Output('auth-output', 'children'),
    Input('login-button', 'n_clicks'),
    State('username', 'value'),
    State('password', 'value'),
    prevent_initial_call=True
)
def login(n_clicks, username, password):
    if username == 'admin' and password == 'admin':
        return {'display': 'block'}, {'display': 'none'}, ''
    else:
        return {'display': 'none'}, {'display': 'block'}, dbc.Alert("Invalid credentials!", color="danger")


# Helper: decode uploaded file
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

# Callback: load file and update controls

@app.callback(
    [
        Output('dataset-store', 'data'),
        Output('data-preview', 'data'),
        Output('data-preview', 'columns'),
        Output('selector', 'options'),
        Output('selector', 'value'),
        Output('sort-column', 'options'),
        Output('sort-column', 'value'),
        Output('filter-column', 'options'),
        Output('filter-column', 'value'),
        Output('filter-slider', 'max'),
        Output('filter-slider', 'marks'),
        Output('filter-slider', 'value'),
        Output('groupby', 'options'), 
        Output('groupby', 'value') 
    ],
    Input('file-upload', 'contents'),
    State('file-upload', 'filename'),
    prevent_initial_call=True
)
def update_output(contents, filename):
    if contents:
        df = load_data(contents, filename)
        data = df.to_dict('records')
        columns = [{'name': col, 'id': col} for col in df.columns]
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        options = [{'label': col, 'value': col} for col in numeric_cols]
        first = numeric_cols[0] if numeric_cols else None
        max_val = df[first].max() if first else 100
        marks = {
            int(v): f'{int(v)}-{int(v + max_val / 10)}'
            for v in np.linspace(0, max_val, 10, dtype=int)
        }

        cat_cols = df.select_dtypes(include='object').columns.tolist()
        groupby_options = [{'label': col, 'value': col} for col in cat_cols]

        return (
            data, data, columns,
            options, first,
            options, first,
            options, first,
            max_val, marks, max_val,
            groupby_options, None
        )

# Callback: update slider label
@app.callback(
    Output('slider-label', 'children'),
    Input('filter-column', 'value')
)
def update_slider_label(col):
    return f"Filter by {col}:" if col else "Filter by selected column:"

# Callback: update graph
@app.callback(
    Output('graph', 'figure'),
    Input('selector', 'value'),
    Input('groupby', 'value'), 
    Input('plot-type', 'value'),
    Input('sort-column', 'value'),
    Input('sort-order', 'value'),
    Input('filter-column', 'value'),
    Input('filter-slider', 'value'),
    State('dataset-store', 'data'),
    prevent_initial_call=True
)
def update_graph(selected_value, groupby_col, plot_type, sort_col, sort_order, filter_col, slider_val, stored_data):
    if stored_data and selected_value:
        df = pd.DataFrame(stored_data)

        if filter_col and slider_val is not None:
            df = df[df[filter_col] <= slider_val]
        if sort_col:
            df = df.sort_values(by=sort_col, ascending=(sort_order == 'asc'))

        kwargs = {'x': selected_value}
        if groupby_col and groupby_col in df.columns:
            kwargs['color'] = groupby_col

        title = f"{plot_type.capitalize()} of {selected_value}"
        if groupby_col:
            title += f" grouped by {groupby_col}"

        if plot_type == 'histogram':
            fig = px.histogram(df, barmode='overlay', nbins=20, title=title, **kwargs)
        elif plot_type == 'bar':
            fig = px.bar(df, title=title, **kwargs)
        elif plot_type == 'line':
            fig = px.line(df, title=title, **kwargs)
        elif plot_type == 'box':
            fig = px.box(df, title=title, **kwargs)
        elif plot_type == 'scatter':
            fig = px.scatter(df, title=title, **kwargs)
        else:
            fig = px.histogram(df, title=title, **kwargs)  # fallback

        fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
        return fig
    return {}

# Callback: download CSV
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

# Run the server
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run(debug=False, host="0.0.0.0", port=port)
