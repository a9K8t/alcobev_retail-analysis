-- 4. Sales by Item Type
SELECT
    item_type,
    ROUND(SUM(retail_sales), 2)      AS total_retail_sales,
    ROUND(SUM(warehouse_sales), 2)   AS total_warehouse_sales,
    ROUND(SUM(retail_transfers), 2)  AS total_retail_transfers,
    COUNT(*)                         AS record_count
FROM sales
GROUP BY item_type
ORDER BY total_retail_sales DESC;
