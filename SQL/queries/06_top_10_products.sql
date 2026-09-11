-- 6. Top 10 Products by Retail Sales Volume
SELECT
    item_description,
    ROUND(SUM(retail_sales), 2) AS total_retail_sales
FROM sales
GROUP BY item_description
ORDER BY total_retail_sales DESC
LIMIT 10;
