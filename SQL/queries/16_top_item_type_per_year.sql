-- 16. Item Type Ranked Within Each Year (Window Function / CTE)
WITH yearly_item_type AS (
    SELECT
        year,
        item_type,
        SUM(retail_sales) AS total_retail_sales
    FROM sales
    GROUP BY year, item_type
),
ranked_item_types AS (
    SELECT
        year,
        item_type,
        ROUND(total_retail_sales, 2) AS total_retail_sales,
        RANK() OVER (PARTITION BY year ORDER BY total_retail_sales DESC) AS rank_in_year
    FROM yearly_item_type
)
SELECT
    year,
    item_type,
    total_retail_sales,
    rank_in_year
FROM ranked_item_types
WHERE rank_in_year <= 3
ORDER BY year, rank_in_year;
