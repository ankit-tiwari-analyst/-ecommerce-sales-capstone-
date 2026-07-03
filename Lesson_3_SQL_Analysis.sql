
-- Load your cleaned data into MySQL (new database, e.g. sales_db). Run the CTE+window function query from Part 5 — paste the top product per category

USE sales_db;

-- CTE + Window function: rank products by profit WITHIN each category
WITH product_profit AS (
    SELECT
        Category,
        Product_Name,
        SUM(Profit) AS total_profit,
        RANK() OVER (
            PARTITION BY Category
            ORDER BY SUM(Profit) DESC
        ) AS profit_rank
    FROM sales
    GROUP BY Category, Product_Name
)
SELECT * FROM product_profit
WHERE profit_rank = 1
ORDER BY total_profit DESC;


-- Write a SQL query joining a State-to-Region lookup you create yourself (like Week 6's class_info) — OR write a query using GROUP BY + HAVING to find categories where average profit margin exceeds 20%

SELECT 
	Category,
    ROUND(AVG(Profit / Revenue) * 100, 2) AS AVG_profit_margin_pct
    FROM sales 
    GROUP BY Category
    HAVING AVG(Profit / Revenue) * 100 > 20
    ORDER BY AVG_profit_margin_pct DESC;





