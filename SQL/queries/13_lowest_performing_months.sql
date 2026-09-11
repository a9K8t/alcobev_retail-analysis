-- 13. Lowest-Performing Months (bottom 5 by retail sales)
SELECT
    year,
    month,
    ROUND(SUM(retail_sales), 2) AS total_retail_sales
FROM sales
GROUP BY year, month
ORDER BY total_retail_sales ASC
LIMIT 5;
