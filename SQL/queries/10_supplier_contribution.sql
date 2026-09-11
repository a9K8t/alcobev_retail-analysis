-- 10. Supplier Contribution (% of total + running cumulative %)
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
