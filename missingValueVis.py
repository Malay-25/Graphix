import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def cap_values(value, lower_bound, upper_bound):
    if value < lower_bound:
        return lower_bound
    elif value > upper_bound:
        return upper_bound
    else:
        return value

data = pd.read_csv('personality_dataset.csv')

data = data.dropna(axis=0, how='any')

numerical_data = data.select_dtypes(include=['float64'])

for col in numerical_data.columns:
    Q1 = numerical_data[col].quantile(0.25)
    Q3 = numerical_data[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    data[col] = data[col].apply(lambda x: cap_values(x, lower_bound, upper_bound))

data.to_csv('cleaned_personality_dataset.csv', index=False)