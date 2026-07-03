
# E-Commerce Sales Analysis — Capstone Project

# Executive Summary

This project analyzes e-commerce sales data to uncover the key factors driving revenue, customer purchasing behavior, and overall business performance. The analysis identifies top-performing products, regions, and customer segments while highlighting trends that can help improve sales and profitability. The findings provide actionable insights for inventory planning, marketing campaigns, and customer retention strategies, enabling data-driven business decisions. By transforming raw sales data into clear visualizations and meaningful recommendations, this project demonstrates how analytics can support sustainable business growth.

## Overview
End-to-end analysis of 200,000 e-commerce transactions
(2023-2024) covering EDA, machine learning, SQL, and
an interactive Power BI dashboard.

## Business Questions Answered
1. Which category generates the highest profit?
2. Which region has the strongest revenue?
3. Does discounting hurt profit margin?
4. Which cities have the most customers?
5. Which products drive the most profit?

## Key Findings
- Home & Furniture leads in profit ($11.22M total)
- East region generates highest revenue ($44.98M)
- Discounting does NOT meaningfully hurt margin
  (25.83% discounted vs 25.72% non-discounted)
- Top product: Tempur-Pedic Mattress ($2.13M profit)

## Machine Learning
Random Forest Regressor predicting order Profit:
- R² Score: 0.827 | MAE: $38.70 | RMSE: $64.97
- Outperforms Linear Regression (R²: 0.715)

## SQL Analysis
MySQL database with window functions and CTEs:
- Top product per category (RANK() OVER PARTITION BY)
- Categories with 20%+ profit margin (GROUP BY + HAVING)

## Tools
Python (Pandas, Seaborn, scikit-learn) | MySQL |
Power BI | Sweetviz

## Dashboard
![Dashboard](dashboard_screenshot.png)
📁 [Download .pbix](sales_dashboard.pbix)

## Author
Ankit Tiwari — Data Analyst
[LinkedIn](https://www.linkedin.com/in/ankit-tiwari-b9b7473b1) | New Delhi, India
