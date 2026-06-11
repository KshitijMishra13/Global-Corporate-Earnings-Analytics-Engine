import pandas as pd
import numpy as np

print("=== Starting Fresh Standalone Star-Schema Pipeline ===")

# 1. Read directly from your raw source dataset file
try:
    df_raw = pd.read_csv('/Users/kshitijmr13/Companies Market Share/companies_by_earnings.csv')
    print("-> Successfully loaded source data from local project directory.")
except FileNotFoundError:
    df_raw = pd.read_csv('/Users/kshitijmr13/Downloads/companies_by_earnings.csv')
    print("-> Successfully loaded source data from Downloads directory.")

# 2. Vectorized Cleaning and Numerical Normalization
df_raw['Stock Price'] = df_raw['Stock Price'].str.replace('$', '', regex=False).str.replace(',', '', regex=False)
df_raw['Stock Price'] = pd.to_numeric(df_raw['Stock Price'], errors='coerce')
df_raw['Raw Earnings ($)'] = df_raw['Raw Earnings ($)'].fillna(0)
df_raw['Earnings_USD_Actual'] = df_raw['Raw Earnings ($)'].astype(float)

# 3. Interquartile Range (IQR) Outlier Engine
q1 = df_raw['Earnings_USD_Actual'].quantile(0.25)
q3 = df_raw['Earnings_USD_Actual'].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

conditions = [
    (df_raw['Earnings_USD_Actual'] > upper_bound),
    (df_raw['Earnings_USD_Actual'] < lower_bound)
]
choice = ['Higher Outlier', 'Lower Outlier']
df_raw['Earnings_Anomalies'] = np.select(conditions, choice, default='Standard')

# 4. Feature Engineering: Corporate Tier Categorization
tier_conditions = [
    (df_raw['Earnings_USD_Actual'] >= 100_000_000_000),
    (df_raw['Earnings_USD_Actual'] >= 50_000_000_000) & (df_raw['Earnings_USD_Actual'] < 100_000_000_000),
    (df_raw['Earnings_USD_Actual'] >= 10_000_000_000) & (df_raw['Earnings_USD_Actual'] < 50_000_000_000),
    (df_raw['Earnings_USD_Actual'] < 10_000_000_000)
]
tier_choice = ['Tier 1', 'Tier 2', 'Tier 3', 'Tier 4']
df_raw['Corporate_Tier'] = np.select(tier_conditions, tier_choice, default='Unclassified')

# 5. Star Schema Separation and Relational Mapping
dim_geography = df_raw[['Country']].drop_duplicates().reset_index(drop=True)
dim_geography['geography_id'] = dim_geography.index + 1001
dim_geography.rename(columns={'Country': 'geography_name'}, inplace=True)

dim_company = df_raw[['Company Name', 'Ticker', 'Corporate_Tier']].drop_duplicates().reset_index(drop=True)
dim_company['company_id'] = dim_company.index + 2001
dim_company.rename(columns={'Company Name': 'Company'}, inplace=True)

fact_matrix = df_raw.merge(dim_geography, left_on='Country', right_on='geography_name', how='left')
fact_matrix = fact_matrix.merge(dim_company, left_on='Ticker', right_on='Ticker', how='left')

fact_earnings = fact_matrix[['company_id', 'geography_id', 'Rank', 'Earnings_USD_Actual', 'Stock Price', 'Earnings_Anomalies']]
fact_earnings.rename(columns={'Rank': 'Global_Rank'}, inplace=True)

# 6. Save Star Schema Files directly to your project workspace folder
print("Writing optimized dimension and fact components to disk...")
dim_geography.to_csv('/Users/kshitijmr13/Companies Market Share/dim_geography.csv', index=False)
dim_company.to_csv('/Users/kshitijmr13/Companies Market Share/dim_company.csv', index=False)
fact_earnings.to_csv('/Users/kshitijmr13/Companies Market Share/fact_earnings.csv', index=False)

print("\n=== SUCCESS: ALL PORTFOLIO MODELING PHASES COMPLETED ===")
print("Files saved perfectly: dim_geography.csv, dim_company.csv, fact_earnings.csv")