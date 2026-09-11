-- 17. Suppliers That Sell Across Most Item Types (Breadth / Diversification)
SELECT
    supplier,
    COUNT(DISTINCT item_type) AS distinct_item_types,
    COUNT(DISTINCT item_description) AS distinct_products,
    ROUND(SUM(retail_sales), 2) AS total_retail_sales
FROM sales
GROUP BY supplier
ORDER BY distinct_item_types DESC, total_retail_sales DESC
LIMIT 10;
