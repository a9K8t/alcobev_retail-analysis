-- 18. Retail vs Warehouse Movement Imbalance Classification
SELECT
    item_type,
    ROUND(SUM(retail_sales), 2)    AS total_retail_sales,
    ROUND(SUM(warehouse_sales), 2) AS total_warehouse_sales,
    CASE
        WHEN SUM(warehouse_sales) = 0 AND SUM(retail_sales) = 0 THEN 'NO ACTIVITY'
        WHEN SUM(warehouse_sales) = 0 THEN 'RETAIL ONLY'
        WHEN SUM(retail_sales) = 0 THEN 'WAREHOUSE ONLY'
        WHEN SUM(retail_sales) > SUM(warehouse_sales) THEN 'RETAIL DOMINANT'
        ELSE 'WAREHOUSE DOMINANT'
    END AS movement_pattern
FROM sales
GROUP BY item_type
ORDER BY total_retail_sales DESC;
