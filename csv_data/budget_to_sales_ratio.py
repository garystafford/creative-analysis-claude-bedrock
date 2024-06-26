# script generated by model to calculate ratio of grand total of ad budgets to sales for ID 100

import pandas as pd

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('advertising_budget_and_sales.csv')

# Select the row with ID 100
row_100 = df.loc[df['Unnamed: 0'] == 100]

# Calculate the sum of TV, radio, and newspaper ad budgets for ID 100
total_ad_budget = row_100['TV Ad Budget ($)'].values[0] + row_100['Radio Ad Budget ($)'].values[0] + row_100['Newspaper Ad Budget ($)'].values[0]

# Get the sales value for ID 100
sales_100 = row_100['Sales ($)'].values[0]

# Calculate the ratio of total ad budget to sales for ID 100
ratio = total_ad_budget / sales_100

print(f"The ratio of the grand total of TV, radio, and newspaper ad budgets to sales for ID 100 is: {ratio:.2f}")