import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go

df = pd.read_csv('cleaned_personality_dataset.csv')

x = df.index

y1 = df['Time_spent_Alone']
y2 = df['Social_event_attendance']
y3 = df['Post_frequency']

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(x, y1, color='#2ecc71', linestyle='-', marker='o', markersize=6, label='Time Spent Alone')
ax.plot(x, y2, color='#e74c3c', linestyle='--', marker='s', markersize=6, label='Social Event Attendance')
ax.plot(x, y3, color='#3498db', linestyle=':', marker='D', markersize=6, label='Post Frequency')

ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

ax.set_title('Participant Behavior Comparison', fontsize=16, fontweight='bold')
ax.set_xlabel('Participant Index', fontsize=12)
ax.set_ylabel('Behavioral Metrics', fontsize=12)

ax.legend(loc='upper right', fontsize=11)

ax.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()

custom_palette = ['#2ecc71', '#e74c3c']  # One for Introvert, one for Extrovert

fig, ax = plt.subplots(figsize=(8, 5))

sns.countplot(x='Personality', hue='Personality', data=df, ax=ax, palette=custom_palette, legend=False)

ax.set_title('Participant Count by Personality Type', fontsize=16, fontweight='bold')
ax.set_xlabel('Personality', fontsize=12)
ax.set_ylabel('Number of Participants', fontsize=12)

for patch in ax.patches:
    height = patch.get_height()
    ax.text(patch.get_x() + patch.get_width()/2, height + 1, str(int(height)), 
            ha='center', va='bottom', fontsize=11)

plt.tight_layout()
plt.show()

x_vals = df.index

fig = go.Figure()

# Time Spent Alone
fig.add_trace(go.Scatter(
    x=x_vals,
    y=df['Time_spent_Alone'],
    name='Time Spent Alone',
    line=dict(color='#2ecc71', width=2, dash='solid'),
    marker=dict(color='#2ecc71', size=6)
))

# Social Event Attendance
fig.add_trace(go.Scatter(
    x=x_vals,
    y=df['Social_event_attendance'],
    name='Social Event Attendance',
    line=dict(color='#e74c3c', width=2, dash='dash'),
    marker=dict(color='#e74c3c', size=6)
))

# Post Frequency
fig.add_trace(go.Scatter(
    x=x_vals,
    y=df['Post_frequency'],
    name='Post Frequency',
    line=dict(color='#3498db', width=2, dash='dot'),
    marker=dict(color='#3498db', size=6)
))

# Layout customization
fig.update_layout(
    title='Behavioral Patterns Across Participants',
    xaxis_title='Participant Index',
    yaxis_title='Score / Frequency',
    font=dict(size=12),
    margin=dict(l=50, r=50, t=50, b=50),
    paper_bgcolor='rgb(255,255,255)',
    plot_bgcolor='rgb(255,255,255)',
    hovermode='x unified'
)

fig.show()