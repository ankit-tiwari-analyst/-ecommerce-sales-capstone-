
# Apply all cleaning from Part 1 — strip columns, drop Country, create Month/Year from Order_Date

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style='whitegrid')
df = pd.read_csv('sales_data.csv')

# --- CLEANING (from Lesson 1 findings) ---
df.columns = df.columns.str.strip()              
df = df.drop(columns=['Country'])              
df['Order_Date'] = pd.to_datetime(df['Order_Date'])
df['Month'] = df['Order_Date'].dt.month
df['Year']  = df['Order_Date'].dt.year

# Verify the fix worked
print(df.columns.tolist())
print(df[['Order_Date', 'Month', 'Year']].head())

df.to_csv('cleaned_sales_data.csv', index=False)


# Run outlier checks on Revenue, Profit, Unit_Price, Quantity — decide and document keep/cap for each

# Reuse your Week 2 IQR function
def iqr_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return ((df[column] < lower) | (df[column] > upper)).sum()

for col in ['Revenue', 'Profit', 'Unit_Price', 'Quantity']:
    count = iqr_outliers(df, col)
    pct = count / len(df) * 100
    print(f'{col}: {count} outliers ({pct:.1f}%)')
    

# Build the univariate 2×2 grid from Part 3, save as PNG

# Univariate: 2x2 grid
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Univariate Analysis - Sales Data', fontsize=16, fontweight='bold')

sns.histplot(df['Revenue'], bins=50, ax=axes[0, 0], color='#3498db')
axes[0, 0].set_title('Revenue Distribution')

sns.histplot(df['Profit'], bins=50, ax=axes[0, 1], color='#9b59b6')
axes[0, 1].set_title('Profit Distribution')

sns.countplot(x='Region', data=df, ax=axes[1, 0],
            order=df['Region'].value_counts().index, color='#2ecc71')
axes[1, 0].set_title('Orders by Region')
axes[1, 0].tick_params(axis='x', rotation=45)

sns.countplot(x='Category', data=df, ax=axes[1, 1],
            order=df['Category'].value_counts().index, color='#e67e22')
axes[1, 1].set_title('Orders by Category')
axes[1, 1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('Capstone_univariate.png', dpi=150, bbox_inches='tight')
# plt.show()


# Answer ALL 5 business questions with code — print results AND create at least 3 charts visualizing them

# Q1: Which category has highest profit?
q1 = df.groupby('Category')['Profit'].sum().sort_values(ascending=False)
print('q1: Profit by Category:\n', q1)

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x=q1.index, y=q1.values, palette='viridis', ax=ax)
ax.set_title('Total profit by category', fontsize=14, fontweight='bold')
ax.set_xlabel('Category')
ax.set_ylabel('Total Profit')
plt.tight_layout()
plt.savefig('Capstone_q1.png', dpi=150, bbox_inches='tight')
plt.show()

# Q2: Which region has highest revenue?
q2 = df.groupby('Region')['Revenue'].sum().sort_values(ascending=False)
print('q2: Revenue by Region:\n', q2)

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x=q2.index, y=q2.values, palette='viridis', ax=ax)
ax.set_title('Total revenue by region', fontsize=14, fontweight='bold')
ax.set_xlabel('Region')
ax.set_ylabel('Total Revenue')
plt.tight_layout()
plt.savefig('Capstone_q2.png', dpi=150, bbox_inches='tight')
plt.show()

# Q3: Does discount (low Unit_Price relative to Revenue/Quantity) correlate with lower profit margins?
product_avg_price = df.groupby('Product_Name')['Unit_Price'].transform('mean')
df['Is_Discounted'] = df['Unit_Price'] < (product_avg_price * 0.9)  # 10%+ below average

print(f"Discounted transactions: {df['Is_Discounted'].sum()} ({df['Is_Discounted'].mean()*100:.1f}%)")

# Now compare profit margin
df['Profit_Margin'] = df['Profit'] / df['Revenue'] * 100

margin_comparison = df.groupby('Is_Discounted')['Profit_Margin'].mean().round(2)
print(margin_comparison)

# Q4: Top 5 cities by customer count
q4 = df.groupby('City')['Customer_Name'].nunique().nlargest(5)
print('\nq4: Top 5 Cities by Unique Customers:\n', q4)

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x=q4.index, y=q4.values, palette='viridis', ax=ax)
ax.set_title('Top 5 cities by unique customers', fontsize=14, fontweight='bold')
ax.set_xlabel('City')
ax.set_ylabel('Number of unique customers')
plt.tight_layout()
plt.savefig('Capstone_q4.png', dpi=150, bbox_inches='tight')
plt.show()

# Q5: Top 5 products by profit
q5 = df.groupby('Product_Name')['Profit'].sum().nlargest(5)
print('\nq5: Top 5 Products by Profit:\n', q5)

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x=q5.index, y=q5.values, palette='viridis', ax=ax)
ax.set_title('Top 5 products by profit', fontsize=14, fontweight='bold')
ax.set_xlabel('Product')
ax.set_ylabel('Profit')
plt.tight_layout()
plt.savefig('Capstone_q5.png', dpi=150, bbox_inches='tight')
plt.show()


# Write a findings summary (like your Week 2 Titanic conclusions) — at least 5 numbered insights with real numbers

''' insights summary: i starting with the top 5 insights from the analysis above. 
1. the category with the highest profit is 'Home & Furniture' with a total profit of $11,218,596.
2. the region with the highest revenue is 'East' with a total revenue of $44,980,048.
3."43.9% of transactions (87,758 orders) were discounted by 10%+ below the product's average price. Surprisingly, discounted transactions had a nearly identical profit margin (25.83%) compared to non-discounted ones (25.72%) — suggesting discounting has not meaningfully hurt profitability in this business."
4. the top 5 cities with the highest number of unique customers are Pittsburgh (2,874), Burlington (2,859), Manchester (2,843), jersey City (2,839), Providence (2,835).
5. the top 5 products by profit are 'Tempur-Pedic Mattress' ($2,134,208), 'Instant Pot' ($1,689,924), 'Nike Air Force 1' ($1,128,698), 'Storage Rack' ($1,052,179), and 'MacBook Air' ($1,028,767).'''


'''CHALLENGE: Investigate the relationship between discount-like patterns (low Unit_Price relative to typical category price) and Profit margin — is there evidence the business loses money on certain pricing patterns?'''

product_avg_price = df.groupby('Product_Name')['Unit_Price'].transform('mean')
df['Is_Discounted'] = df['Unit_Price'] < (product_avg_price * 0.9)  # 10%+ below average

print(f"Discounted transactions: {df['Is_Discounted'].sum()} ({df['Is_Discounted'].mean()*100:.1f}%)")

# Now compare profit margin
df['Profit_Margin'] = df['Profit'] / df['Revenue'] * 100

margin_comparison = df.groupby('Is_Discounted')['Profit_Margin'].mean().round(2)
print(margin_comparison)

num_col = df[['Revenue', 'Profit', 'Unit_Price', 'Quantity']]
corr = num_col.corr()

fig, ax = plt.subplots(figsize=(9, 7))

sns.heatmap(
    corr,
    annot=True,
    fmt='.2f',
    cmap='coolwarm',
    center=0,
    linewidths=0.5,
    ax=ax
)

ax.set_title('correlation heatmap sales data' , fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('Capstone_correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.show()










