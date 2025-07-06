import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('cleaned_personality_dataset.csv')

fig1 = px.line(df, 
              x=df.index, 
              y='Time_spent_Alone', 
              title='Trend of Time Spent Alone Across Participants',
              labels={'x': 'Participant', 'y': 'Time Spent Alone'})

# Customize the interactive chart
fig1.update_layout(
    xaxis=dict(
        showgrid=True,
        gridwidth=0.5,
        gridcolor='lightgray'),
    yaxis=dict(
        showgrid=True,
        gridwidth=0.5,
        gridcolor='lightgray'),
    margin=dict(l=20, r=20, t=40, b=20),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

grouped = df.groupby('Personality')['Friends_circle_size'].mean().reset_index()

fig2 = px.bar(grouped, x='Personality', y='Friends_circle_size',
             color='Personality', text_auto='.2f',
             title='Average Friends Cricle Size by Personality')
fig2.update_layout(yaxis_title='Average Friend Circle Size')

# Initialize the Dash app
app = dash.Dash(__name__)

# Create the layout
app.layout = html.Div(children=[
    html.H1(children='Time Spent Alone & Friends Circle Size Dashboard'),
    
    html.Div([
        html.Div([
            dcc.Graph(id='tsa-graph', figure=fig1)
        ], style={'width': '49%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id='fcs-graph', figure=fig2)
        ], style={'width': '49%', 'display': 'inline-block'})
    ])
])

if __name__ == '__main__':
    app.run(debug=True)