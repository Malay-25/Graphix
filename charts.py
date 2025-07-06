import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv('cleaned_personality_dataset.csv')

# Create a simple line chart
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['Time_spent_Alone'], 
         color='blue', 
         marker='o', 
         linestyle='-', 
         linewidth=2,
         markersize=4)

# Customize the chart
plt.title('Trend of Time Spent Alone Across Participants', fontsize=14, fontweight='bold')
plt.xlabel('Participant', fontsize=12)
plt.ylabel('Time Spent Alone', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Create a line chart using Seaborn
plt.figure(figsize=(10, 6))
sns.lineplot(x=df.index, y='Time_spent_Alone', data=df, 
             color='navy', 
             linewidth=2,
             marker='o',
             markersize=4)

# Customize the chart
plt.title('Trend of Time Spent Alone Across Participants', fontsize=14, fontweight='bold')
plt.xlabel('Participant', fontsize=12)
plt.ylabel('Time Spent Alone', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Create an interactive line chart with Plotly
fig = px.line(df, 
              x=df.index, 
              y='Time_spent_Alone', 
              title='Trend of Time Spent Alone Across Participants',
              labels={'x': 'Participant', 'y': 'Time Spent Alone'})

# Customize the interactive chart
fig.update_layout(
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

fig.show()

grouped = df.groupby('Personality')['Time_spent_Alone'].mean()

grouped.plot(kind='line', marker='o', title='Avg. Time Spent Alone by Personality')
plt.xlabel('Personality')
plt.ylabel('Average Time Spent Alone')
plt.grid(True)
plt.tight_layout()
plt.show()

# Save as PNG
#plt.savefig('line_chart_matplotlib.png', dpi=300, bbox_inches='tight')

# Save as SVG
#plt.savefig('line_chart_matplotlib.svg', bbox_inches='tight')