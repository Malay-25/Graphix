import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

tips = sns.load_dataset("tips")

#Basic Summary Statistics
basic_stats = tips.describe()
print("Basic Statistics:")
print(basic_stats)

#Central Tendency Measures
mean_total = tips['total_bill'].mean()
print(f"\nMean of Total Bill: {mean_total:.2f}")

median_tip = tips['tip'].median()
print(f"Median of Tip: {median_tip:.2f}")

mode_sex = tips['sex'].mode()[0]
print(f"Mode of Sex: {mode_sex}")

#Dispersion Measures
range_total = tips['total_bill'].max() - tips['total_bill'].min()
print(f"\nRange of Total Bill: {range_total:.2f}")

variance_tip = tips['tip'].var()
print(f"Variance of Tip: {variance_tip:.2f}")

std_total = tips['total_bill'].std()
print(f"Standard Deviation of Total Bill: {std_total:.2f}")

#Distribution Shape
skew_total = tips['total_bill'].skew()
print(f"\nSkewness of Total Bill: {skew_total:.2f}")

kurtosis_tip = tips['tip'].kurtosis()
print(f"Kurtosis of Tip: {kurtosis_tip:.2f}")

#Visualizing the data distribution
plt.figure(figsize=(10, 6))

plt.subplot(1, 2, 1)
sns.boxplot(tips['total_bill'])
plt.title("Boxplot of Total Bill")
plt.xlabel("Total Bill ($)")

plt.subplot(1, 2, 2)
sns.histplot(tips['tip'], bins=10, kde=True)
plt.title("Histogram of Tip")
plt.xlabel("Tip ($)")

plt.tight_layout()
plt.show()

#Correlation between Variables
corr_matrix = tips[['total_bill', 'tip', 'size']].corr()
print("\nCorrelation Matrix:")
print(corr_matrix)

plt.figure(figsize=(6, 4))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
plt.title("Correlation Matrix")
plt.show()