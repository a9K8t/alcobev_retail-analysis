-- 14. Lowest-Performing Item Types (min 50 records)
SELECT
    item_type,
    ROUND(SUM(retail_sales), 2) AS total_retail_sales,
    COUNT(*) AS record_count
FROM sales
GROUP BY item_type
HAVING COUNT(*) >= 50
ORDER BY total_retail_sales ASC
LIMIT 10;
