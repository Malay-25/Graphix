import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('cleaned_personality_dataset.csv')

x_axis = df.index

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x_axis,
    y=df['Time_spent_Alone'],
    name='Time Spent Alone',
    line=dict(color='blue'),
    hovertemplate='Participant %{x}<br>%{y} hrs alone<extra></extra>'
))

fig.add_trace(go.Scatter(
    x=x_axis,
    y=df['Social_event_attendance'],
    name='Social Event Attendance',
    line=dict(color='green'),
    hovertemplate='Participant %{x}<br>%{y} events<extra></extra>'
))

fig.add_trace(go.Scatter(
    x=x_axis,
    y=df['Post_frequency'],
    name='Post Frequency',
    line=dict(color='purple'),
    hovertemplate='Participant %{x}<br>%{y} posts<extra></extra>'
))

# Layout
fig.update_layout(
    xaxis=dict(
        rangeslider=dict(visible=True),
        type='linear'
    ),
    title='Behavioral Patterns Across Participants',
    xaxis_title='Participant Index',
    yaxis_title='Score / Count',
    hovermode='x unified',
    template='plotly_white'
)

fig.show()

# Sample data (using COVID-19 data as an example)
dates = ['2020-01', '2020-02', '2020-03', '2020-04', '2020-05']
confirmed_cases = [1000, 2000, 3000, 4000, 5000]
deaths = [50, 100, 150, 200, 250]

# Create a line chart
fig = go.Figure()

# Add confirmed cases trace
fig.add_trace(go.Scatter(
    x=dates,
    y=confirmed_cases,
    name='Confirmed Cases',
    line=dict(color='blue'),
    hovertemplate='%{x}<br>%{y} cases<extra></extra>'
))

# Add deaths trace
fig.add_trace(go.Scatter(
    x=dates,
    y=deaths,
    name='Deaths',
    line=dict(color='red'),
    hovertemplate='%{x}<br>%{y} deaths<extra></extra>'
))

# Update layout for better presentation
fig.update_layout(
    title='COVID-19 Cases Over Time',
    xaxis_title='Date',
    yaxis_title='Number of Cases',
    hovermode='x unified',
    template='plotly_white'
)

# Show the plot
fig.show()