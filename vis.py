import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv('cleaned_personality_dataset.csv')

fig, axes = plt.subplots(2, 2, figsize=(20, 15))

#Histogram
sns.histplot(df['Time_spent_Alone'], ax=axes[0,0],
             bins=10, kde=True, color='skyblue')
axes[0,0].set_title('Histogram of Time Spent Alone')
axes[0,0].set_xlabel('Hours')
axes[0,0].set_ylabel('Frequency')

#Box Plot
sns.boxplot(data=df['Friends_circle_size'], ax=axes[0,1],
            orient='v', color='lightgreen')
axes[0,1].set_title('Box Plot of Friends Circle Size')
axes[0,1].set_ylabel('Size')

#Violin Plot
sns.violinplot(data=df['Post_frequency'], ax=axes[1,0],
               orient='v', color='salmon')
axes[1,0].set_title('Violin Plot of Social Media Post Frequency')
axes[1,0].set_ylabel('Frequency')

#Pair Plot (for multiple variables)
numeric_columns = ['Time_spent_Alone', 'Social_event_attendance', 'Going_outside']
sns.pairplot(df[numeric_columns + ['Drained_after_socializing']],
             hue='Drained_after_socializing',
             diag_kind='kde', palette='husl', markers=['o', 's'])

plt.tight_layout()
plt.show()