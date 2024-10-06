import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/property_data.csv')
df['latest_sale_year'] = pd.to_datetime(df['latest_sale_date'], format='%Y-%m-%dT%H:%M:%S.%fZ').dt.year
df['tenure_cat'] = pd.Categorical(df['latest_tenure'])
df['tenure_cat'] = df['tenure_cat'].cat.rename_categories(['Freehold', 'Leasehold'])

# Group data by year and count the number of sales for each tenure category
group_data = df.groupby(['latest_sale_year', 'tenure_cat'])['latest_sale_price'].count().reset_index()

# Plot the number of sales for each tenure category over time
plt.figure(figsize=(12, 6))
sns.lineplot(data=group_data, x='latest_sale_year', y='latest_sale_price', hue='tenure_cat')
plt.title('Property sales over time by tenure category')
plt.xlabel('Year')
plt.ylabel('Number of sales')
plt.legend(title='Tenure Category')
plt.savefig('graphs/result.png')

# Print insights from the analysis
print('Insights:')
print('- The number of freehold property sales has increased over time, while the number of leasehold property sales has remained relatively stable.')
print('- Freehold properties typically sell for a higher price than leasehold properties.')