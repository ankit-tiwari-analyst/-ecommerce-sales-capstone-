# import kagglehub

# # Download latest version
# path = kagglehub.dataset_download("yashyennewar/product-sales-dataset-2023-2024")

# print("Path to dataset files:", path)


'''Load the dataset, run the full overview block — paste your df.shape and df.columns.tolist() output here'''

# =============================================
# E-COMMERCE SALES CAPSTONE PROJECT
# Author: Ankit Tiwari   Date: June 2026
# Dataset: Product Sales Dataset 2023-2024
# =============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style='whitegrid')

df = pd.read_csv('sales_data.csv')

df.columns = df.columns.str.strip()

# === PHASE 1: OVERVIEW ===
print('='*50)
print('DATASET OVERVIEW')
print('='*50)
print(f'shape: {df.shape}')
print(f'columns: {df.columns.tolist()}')
print('\nfirst 5 rows:')
print(df.head())
print('\nData types:')
print(df.dtypes)
print('\nmissing values:')
print(df.isnull().sum())
print('\nBasic stats:')
print(df.describe().round(2))

shape: (200000, 14)
columns: ['Order_ID', 'Order_Date', 'Customer_Name', 'City', 'State', 'Region', 'Country',
 'Category', 'Sub_Category', 'Product_Name', 'Quantity', ' Unit_Price ', ' Revenue ', ' Profit ']


'''Answer the 5 understanding questions from Part 2 in your own words'''

# 1. What does one ROW represent?
# Row represent order_id, order_date, coustomer_name, state, country, category, revenue, profit ect.

# 2. What is the time range? 
# A dataset represent 2023 to 2024 sales by varius factors.

# 3. Which columns are numeric vs categorical?
# Order_ID           int64
# Order_Date        object
# Customer_Name     object
# City              object
# State             object
# Region            object
# Country           object
# Category          object
# Sub_Category      object
# Product_Name      object
# Quantity           int64
#  Unit_Price      float64
#  Revenue         float64
#  Profit          float64

# 4. Are there any obvious data quality issues? 
# no there is not any data quality issue.

# 5. Which 3 columns are most important for answering your 5 business questions?
# the most important columns are 'Category', 'Revenue', 'Profit' for answering business questions.


'''Run sweetviz — find and explain 3 specific flagged findings with exact numbers'''

import sweetviz as sv

report = sv.analyze(df)
report.show_html('sales_sweetviz.html')
print("✓ Report saved")

# finding 1: 29% of total orders around 57000 are from East region.
# finding 2: 31% of total orders around 62000 for Clothing & Apparel.
# finding 3: 75% of revenue from 100 to 400 worth of product.


'''Run the 5 groupby operations from Part 4 (with corrected column names) — paste the top-category and top-region results'''

# 1. Total revenue by category
print(df.groupby('Category')['Revenue'].sum().sort_values(ascending=False))

# 2. Average profit margin by category
print(df.groupby('Category')['Profit'].mean().round(2))

# 3. Sales by region
print(df.groupby('Region')['Revenue'].sum().sort_values(ascending=False))

# 4. Monthly revenue trend
df['Order_Date'] = pd.to_datetime(df['Order_Date'])
df['Month'] = df['Order_Date'].dt.month
df['Year']  = df['Order_Date'].dt.year

print(df.groupby('Month')['Revenue'].sum())

# 5. Top 5 products by revenue
print(df.groupby('Product_Name')['Revenue'].sum().nlargest(5))


'''Write your 5 business questions tailored to THIS specific dataset's columns (refine the questions I gave you if needed based on what columns actually exist)'''

# Q1. which category generate highest profit?
# Q2. which region have highest revenue?
# Q3. "Does discount (low Unit_Price relative to Revenue/Quantity) correlate with lower profit margins? Is the business losing money on discounted products?"
# Q4. top 5 city where we have highest number of coustomers?
# Q5. top 5 product with higest profit?


'''CHALLENGE: Find ONE surprising finding from your initial exploration that you didn't expect — something that would change the direction of your analysis or raise a question worth investigating further'''

# in this dataset country column have only one country united states which does not make any sense in analysis. there is no comparision between countrys .

df = df.drop(columns=['Country'])
df.to_csv('cleaned_sales_data.csv', index=False)
