-- 8. Yearly Sales (Retail / Warehouse / Transfers)
SELECT
    year,
    ROUND(SUM(retail_sales), 2)     AS total_retail_sales,
    ROUND(SUM(warehouse_sales), 2)  AS total_warehouse_sales,
    ROUND(SUM(retail_transfers), 2) AS total_retail_transfers
FROM sales
GROUP BY year
ORDER BY year;
