-- 11. Product Contribution (% of total, top 20)
WITH product_totals AS (
    SELECT
        item_description,
        SUM(retail_sales) AS product_retail_sales
    FROM sales
    GROUP BY item_description
),
grand_total AS (
    SELECT SUM(retail_sales) AS total_retail_sales FROM sales
)
SELECT
    pt.item_description,
    ROUND(pt.product_retail_sales, 2) AS retail_sales,
    ROUND(pt.product_retail_sales * 100.0 / gt.total_retail_sales, 3) AS pct_of_total
FROM product_totals pt
CROSS JOIN grand_total gt
ORDER BY pt.product_retail_sales DESC
LIMIT 20;
