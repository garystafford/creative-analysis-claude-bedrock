# script generated by model to calculate total sales

import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('advertising_budget_and_sales.csv')

# Calculate the total sales
total_sales = df['Sales ($)'].sum()

# Print the total sales
print(f"The total sales is: ${total_sales:.2f}")
