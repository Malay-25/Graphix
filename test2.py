import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Sample data
data = {
    'Year': [2015, 2016, 2017, 2018, 2019, 2020],
    'Sales': [100, 120, 140, 160, 180, 200],
    'Expenses': [50, 60, 70, 80, 90, 100],
    'Region': ['North', 'North', 'South', 'South', 'East', 'East']
}

df = pd.DataFrame(data)

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Sales Dashboard'),
    
    html.Div(children='''
        Interactive Sales Dashboard
    '''),
    
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='region-dropdown',
                options=[
                    {'label': i, 'value': i} for i in df['Region'].unique()
                ],
                value='North'
            )
        ], style={'width': '49%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Slider(
                id='year-slider',
                min=df['Year'].min(),
                max=df['Year'].max(),
                value=df['Year'].min(),
                step=None,
                marks={
                    int(year): str(year) for year in df['Year'].unique()
                }
            )
        ], style={'width': '49%', 'display': 'inline-block'})
    ]),
    
    html.Br(),
    
    html.Div([
        html.Div([
            dcc.Graph(id='sales-graph')
        ], style={'width': '49%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id='expenses-graph')
        ], style={'width': '49%', 'display': 'inline-block'})
    ])
])

@app.callback(
    Output('sales-graph', 'figure'),
    [Input('region-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_sales_graph(selected_region, selected_year):
    filtered_df = df[(df['Region'] == selected_region) & 
                     (df['Year'] == selected_year)]
    
    fig = px.bar(filtered_df, x='Year', y='Sales', 
                 title=f'Sales in {selected_region} ({selected_year})',
                 color_discrete_sequence=['#7F7F7F'])
    return fig

@app.callback(
    Output('expenses-graph', 'figure'),
    [Input('region-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_expenses_graph(selected_region, selected_year):
    filtered_df = df[(df['Region'] == selected_region) &
                     (df['Year'] == selected_year)]
    
    fig = px.scatter(filtered_df, x='Year', y='Expenses', 
                  title=f'Expenses in {selected_region} ({selected_year})',
                  color_discrete_sequence=['#E74D4D'])
    return fig

if __name__ == '__main__':
    app.run(debug=True)