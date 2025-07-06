import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

df = pd.read_csv('cleaned_personality_dataset.csv')

df_encoded = df.copy()

df_encoded['Stage_fear'] = df_encoded['Stage_fear'].map({'No': 0, 'Yes': 1})
df_encoded['Drained_after_socializing'] = df_encoded['Drained_after_socializing'].map({'No': 0, 'Yes': 1})
df_encoded['Personality'] = df_encoded['Personality'].map({'Extrovert': 0, 'Introvert': 1})

correlation_matrix = df_encoded.corr()

plt.figure(figsize=(8, 6))
sns.heatmap(
    correlation_matrix, 
    annot=True, 
    cmap='coolwarm', 
    center=0,
    square=True  
)
plt.title('Correlation Matrix Heatmap')
plt.show()

fig = go.Figure(data=go.Heatmap(
    z=correlation_matrix.values,
    x=correlation_matrix.columns,
    y=correlation_matrix.index,
    colorscale='Viridis',
    reversescale=False,
    showscale=True
))

fig.update_layout(title='Interactive Correlation Matrix Heatmap',
                  width=800, height=600)
fig.show()
