-- 7. Monthly Retail Sales
SELECT
    year,
    month,
    ROUND(SUM(retail_sales), 2) AS total_retail_sales
FROM sales
GROUP BY year, month
ORDER BY year, month;
