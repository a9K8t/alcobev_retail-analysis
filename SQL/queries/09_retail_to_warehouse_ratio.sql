-- 9. Retail vs Warehouse Yearly Ratio
SELECT
    year,
    ROUND(SUM(retail_sales), 2)    AS total_retail_sales,
    ROUND(SUM(warehouse_sales), 2) AS total_warehouse_sales,
    CASE
        WHEN SUM(warehouse_sales) = 0 THEN NULL
        ELSE ROUND(SUM(retail_sales) * 1.0 / SUM(warehouse_sales), 4)
    END AS retail_to_warehouse_ratio
FROM sales
GROUP BY year
ORDER BY year;
