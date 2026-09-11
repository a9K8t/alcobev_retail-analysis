-- ================================================================
-- analysis.sql
-- Retail & Warehouse Sales Analytics — Full SQL Analysis Suite
-- Database: SQLite (SQL/database.db), table: sales
-- ================================================================
-- Run with:  python SQL/load_data.py (creates DB and executes queries)
-- Or open individual queries in the queries/ folder.
-- ================================================================


-- ----------------------------------------------------------------
-- 1. TOTAL RETAIL SALES VOLUME
-- ----------------------------------------------------------------
SELECT ROUND(SUM(retail_sales), 2) AS total_retail_sales_volume
FROM sales;


-- ----------------------------------------------------------------
-- 2. TOTAL WAREHOUSE SALES VOLUME
-- ----------------------------------------------------------------
SELECT ROUND(SUM(warehouse_sales), 2) AS total_warehouse_sales_volume
FROM sales;


-- ----------------------------------------------------------------
-- 3. TOTAL RETAIL TRANSFERS VOLUME
-- ----------------------------------------------------------------
SELECT ROUND(SUM(retail_transfers), 2) AS total_retail_transfers_volume
FROM sales;


-- ----------------------------------------------------------------
-- 4. SALES BY ITEM TYPE
-- ----------------------------------------------------------------
SELECT
    item_type,
    ROUND(SUM(retail_sales), 2)      AS total_retail_sales,
    ROUND(SUM(warehouse_sales), 2)   AS total_warehouse_sales,
    ROUND(SUM(retail_transfers), 2)  AS total_retail_transfers,
    COUNT(*)                         AS record_count
FROM sales
GROUP BY item_type
ORDER BY total_retail_sales DESC;


-- ----------------------------------------------------------------
-- 5. TOP 10 SUPPLIERS BY RETAIL SALES VOLUME
-- ----------------------------------------------------------------
SELECT
    supplier,
    ROUND(SUM(retail_sales), 2) AS total_retail_sales
FROM sales
GROUP BY supplier
ORDER BY total_retail_sales DESC
LIMIT 10;


-- ----------------------------------------------------------------
-- 6. TOP 10 PRODUCTS BY RETAIL SALES VOLUME
-- ----------------------------------------------------------------
SELECT
    item_description,
    ROUND(SUM(retail_sales), 2) AS total_retail_sales
FROM sales
GROUP BY item_description
ORDER BY total_retail_sales DESC
LIMIT 10;


-- ----------------------------------------------------------------
-- 7. MONTHLY RETAIL SALES
-- ----------------------------------------------------------------
SELECT
    year,
    month,
    ROUND(SUM(retail_sales), 2) AS total_retail_sales
FROM sales
GROUP BY year, month
ORDER BY year, month;


-- ----------------------------------------------------------------
-- 8. YEARLY SALES (Retail / Warehouse / Transfers)
-- ----------------------------------------------------------------
SELECT
    year,
    ROUND(SUM(retail_sales), 2)     AS total_retail_sales,
    ROUND(SUM(warehouse_sales), 2)  AS total_warehouse_sales,
    ROUND(SUM(retail_transfers), 2) AS total_retail_transfers
FROM sales
GROUP BY year
ORDER BY year;


-- ----------------------------------------------------------------
-- 9. RETAIL VS WAREHOUSE (yearly ratio, using CASE to avoid /0)
-- ----------------------------------------------------------------
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


-- ----------------------------------------------------------------
-- 10. SUPPLIER CONTRIBUTION (% of total + running cumulative %)
--     Uses a window function for the cumulative percentage.
-- ----------------------------------------------------------------
WITH supplier_totals AS (
    SELECT
        supplier,
        SUM(retail_sales) AS supplier_retail_sales
    FROM sales
    GROUP BY supplier
),
grand_total AS (
    SELECT SUM(retail_sales) AS total_retail_sales FROM sales
)
SELECT
    st.supplier,
    ROUND(st.supplier_retail_sales, 2) AS retail_sales,
    ROUND(st.supplier_retail_sales * 100.0 / gt.total_retail_sales, 3) AS pct_of_total,
    ROUND(
        SUM(st.supplier_retail_sales) OVER (
            ORDER BY st.supplier_retail_sales DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) * 100.0 / gt.total_retail_sales,
        3
    ) AS cumulative_pct
FROM supplier_totals st
CROSS JOIN grand_total gt
ORDER BY st.supplier_retail_sales DESC
LIMIT 20;


-- ----------------------------------------------------------------
-- 11. PRODUCT CONTRIBUTION (% of total, top 20)
-- ----------------------------------------------------------------
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


-- ----------------------------------------------------------------
-- 12. HIGHEST-PERFORMING MONTHS (top 5 by retail sales)
-- ----------------------------------------------------------------
SELECT
    year,
    month,
    ROUND(SUM(retail_sales), 2) AS total_retail_sales
FROM sales
GROUP BY year, month
ORDER BY total_retail_sales DESC
LIMIT 5;


-- ----------------------------------------------------------------
-- 13. LOWEST-PERFORMING MONTHS (bottom 5 by retail sales)
-- ----------------------------------------------------------------
SELECT
    year,
    month,
    ROUND(SUM(retail_sales), 2) AS total_retail_sales
FROM sales
GROUP BY year, month
ORDER BY total_retail_sales ASC
LIMIT 5;


-- ----------------------------------------------------------------
-- 14. LOWEST-PERFORMING ITEM TYPES (min 50 records, avoids noise)
-- ----------------------------------------------------------------
SELECT
    item_type,
    ROUND(SUM(retail_sales), 2) AS total_retail_sales,
    COUNT(*) AS record_count
FROM sales
GROUP BY item_type
HAVING COUNT(*) >= 50
ORDER BY total_retail_sales ASC
LIMIT 10;


-- ----------------------------------------------------------------
-- 15. ADVANCED: Year-over-Year Growth Rate in Retail Sales
--     Uses LAG() window function to compare each year to the prior one.
-- ----------------------------------------------------------------
WITH yearly AS (
    SELECT
        year,
        SUM(retail_sales) AS total_retail_sales
    FROM sales
    GROUP BY year
)
SELECT
    year,
    ROUND(total_retail_sales, 2) AS total_retail_sales,
    ROUND(LAG(total_retail_sales) OVER (ORDER BY year), 2) AS prior_year_sales,
    CASE
        WHEN LAG(total_retail_sales) OVER (ORDER BY year) IS NULL THEN NULL
        ELSE ROUND(
            (total_retail_sales - LAG(total_retail_sales) OVER (ORDER BY year))
            * 100.0 / LAG(total_retail_sales) OVER (ORDER BY year),
            2
        )
    END AS yoy_growth_pct
FROM yearly
ORDER BY year;


-- ----------------------------------------------------------------
-- 16. ADVANCED: Item type ranked WITHIN each year (window function
--     RANK partitioned by year) -- "which item type led each year?"
--     Uses a CTE with WHERE filter for SQLite 3.50+ compatibility.
-- ----------------------------------------------------------------
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


-- ----------------------------------------------------------------
-- 17. ADVANCED: Suppliers that sell across the most item types
--     (breadth of catalog / diversification)
-- ----------------------------------------------------------------
SELECT
    supplier,
    COUNT(DISTINCT item_type) AS distinct_item_types,
    COUNT(DISTINCT item_description) AS distinct_products,
    ROUND(SUM(retail_sales), 2) AS total_retail_sales
FROM sales
GROUP BY supplier
ORDER BY distinct_item_types DESC, total_retail_sales DESC
LIMIT 10;


-- ----------------------------------------------------------------
-- 18. ADVANCED: Retail vs Warehouse imbalance per item type
--     (CASE-based classification of movement pattern)
-- ----------------------------------------------------------------
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
