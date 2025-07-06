import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

tips = sns.load_dataset("tips")

basic_stats = tips.describe()
#print("Basic Statistics:")
#print(basic_stats)

mean_total = tips['total_bill'].mean()
print(f"\nMean of Total Bill: {mean_total:.2f}")

median_tip = tips['tip'].median()
print(f"Median of Tip: {median_tip:.2f}")

mode_sex = tips['sex'].mode()[0]
print(f"Mode of Sex: {mode_sex}")