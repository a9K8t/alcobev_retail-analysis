-- 15. Year-over-Year Growth Rate in Retail Sales
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
