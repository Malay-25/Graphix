import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('cleaned_personality_dataset.csv')

df_encoded = df.copy()

df_encoded['Stage_fear'] = df_encoded['Stage_fear'].map({'No': 0, 'Yes': 1})
df_encoded['Drained_after_socializing'] = df_encoded['Drained_after_socializing'].map({'No': 0, 'Yes': 1})
df_encoded['Personality'] = df_encoded['Personality'].map({'Extrovert': 0, 'Introvert': 1})

correlation_matrix = df_encoded.corr()

print(correlation_matrix)

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm',
            linecolor='lightgray', linewidths=0.5)
plt.title('Correlation Matrix')
plt.tight_layout()
plt.show()