
# One-hot encode Category and Region, build your feature/target split predicting Profit
import pandas as pd

df = pd.read_csv('cleaned_sales_data.csv')

# One-hot encoding: turns each category into its own 0/1 column
df_encoded = pd.get_dummies(df, columns=['Category', 'Region'], drop_first=True)
print(df_encoded.columns.tolist())


# Print feature_importances_ from your Random Forest — which feature predicts Profit best?

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

# Select feature columns (adjust to your actual encoded column names)
feature_cols = ['Quantity', 'Unit_Price'] + \
    [col for col in df_encoded.columns if col.startswith('Category_') or col.startswith('Region_')]

X = df_encoded[feature_cols]
y = df_encoded['Profit']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Model 1: Linear Regression (simple, interpretable)
lr = LinearRegression()
lr.fit(X_train, y_train)
lr_predictions = lr.predict(X_test)

# Model 2: Random Forest Regressor (usually more accurate)
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
rf_predictions = rf.predict(X_test)

importance_df = pd.DataFrame({
    'feature': feature_cols,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)

print(importance_df)

# Train both LinearRegression and RandomForestRegressor, report MAE/RMSE/R² for both

from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

for name, preds in [('Linear Regression', lr_predictions), ('Random Forest', rf_predictions)]:
    mae = mean_absolute_error(y_test, preds)
    rmse = root_mean_squared_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    print(f"{name}:")
    print(f"  MAE:  ${mae:.2f}")
    print(f"  RMSE: ${rmse:.2f}")
    print(f"  R2:   {r2:.3f}")


# Load your cleaned data into MySQL (new database, e.g. sales_db). Run the CTE+window function query from Part 5 — paste the top product per category
import mysql.connector
from sqlalchemy import create_engine

engine = create_engine(
    'mysql+mysqlconnector://root:12345678@localhost/sales_db'
)

df = pd.read_csv('cleaned_sales_data.csv')
df.to_sql('sales', con=engine, if_exists='replace', index=False)
print("✓ sales table loaded into MySQL")


# CHALLENGE: Predict profit for 3 hypothetical NEW orders you invent (different category, region, quantity, unit price combinations) using your trained Random Forest model

def predict_new_order(category, region, quantity, unit_price, feature_cols, model):
    # Start with a row of all zeros, matching your training columns exactly
    new_order = pd.DataFrame(0, index=[0], columns=feature_cols)
    
    # Set the numeric values
    new_order['Quantity'] = quantity
    new_order['Unit_Price'] = unit_price
    
    # Set the matching one-hot column to 1 (if it exists in feature_cols)
    cat_col = f'Category_{category}'
    if cat_col in feature_cols:
        new_order[cat_col] = 1
    
    reg_col = f'Region_{region}'
    if reg_col in feature_cols:
        new_order[reg_col] = 1
    
    prediction = model.predict(new_order)[0]
    return prediction

# Order 1: expensive electronics, single item
p1 = predict_new_order('Electronics', 'West', quantity=1, unit_price=899.99,
                         feature_cols=feature_cols, model=rf)

# Order 2: mid-range clothing, small bulk
p2 = predict_new_order('Clothing & Apparel', 'South', quantity=5, unit_price=45.00,
                         feature_cols=feature_cols, model=rf)

# Order 3: cheap accessories, large bulk order
p3 = predict_new_order('Accessories', 'East', quantity=20, unit_price=8.50,
                         feature_cols=feature_cols, model=rf)

print(f"Order 1 predicted profit: ${p1:.2f}")
print(f"Order 2 predicted profit: ${p2:.2f}")
print(f"Order 3 predicted profit: ${p3:.2f}")


