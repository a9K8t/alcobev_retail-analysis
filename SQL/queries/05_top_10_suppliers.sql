-- 5. Top 10 Suppliers by Retail Sales Volume
SELECT
    supplier,
    ROUND(SUM(retail_sales), 2) AS total_retail_sales
FROM sales
GROUP BY supplier
ORDER BY total_retail_sales DESC
LIMIT 10;
