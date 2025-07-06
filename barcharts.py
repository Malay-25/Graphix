import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.express as px

df = pd.read_csv('cleaned_personality_dataset.csv')

grouped = df.groupby('Personality')['Time_spent_Alone'].mean()

plt.bar(grouped.index, grouped.values, color=['navy', 'skyblue'])
plt.xlabel('Personality')
plt.ylabel('Average Time Spent Alone')
plt.title('Average Time Spent Alone by Personality')
plt.grid(axis='y')
plt.tight_layout()
plt.show()

sns.barplot(x='Personality', y='Time_spent_Alone', hue='Personality', 
            data=df, estimator='mean', palette='pastel', legend=False)
plt.title('Average Time Spent Alone by Personality')
plt.grid(axis='y')
plt.tight_layout()
plt.show()

grouped = df.groupby('Personality')['Time_spent_Alone'].mean().reset_index()

fig = px.bar(grouped, x='Personality', y='Time_spent_Alone',
             color='Personality', text_auto='.2f',
             title='Average Time Spent Alone by Personality')
fig.update_layout(yaxis_title='Average Time Spent Alone')
fig.show()

