# Interview Preparation: Technical & Business Q&A

Comprehensive interview questions and technically rigorous answers based on the **Retail & Warehouse Sales Analytics** project.

---

## 1. Data Engineering & Cleaning

### Q: "Walk me through how you handled data quality issues, missing values, and anomalies in this dataset."
**Answer**:
> "During initial data profiling of the 307,645 raw records, I identified three categories of missing values:
> 1. **Retail Sales**: Only 3 records had null values in `RETAIL SALES`. Because retail sales was a primary target metric and these exact 3 records were also missing supplier data, I dropped them, arriving at 307,642 records.
> 2. **Supplier**: 164 remaining records lacked a supplier name. Dropping them would discard valid sales volume, so I imputed them with `'Unknown'`.
> 3. **Item Type**: Exactly 1 record (row 96129) had a missing item type for a Barolo wine SKU. I imputed this with `'Unknown'` to preserve volume without making arbitrary categorical assumptions.
> 
> Furthermore, I discovered negative numeric values across Retail Sales (113 records), Transfers (1,016 records), and Warehouse Sales (716 records). Rather than treating these as data corruption and filtering them out, I recognized that they represent legitimate return transactions, keg deposit reversals, and reverse warehouse transfers. Preserving them was essential to calculating true net movement."

---

## 2. Business Semantics & Integrity

### Q: "Why didn't you calculate dollar revenue, profit, or inventory turnover?"
**Answer**:
> "That was an explicit data governance decision. The dataset fields—`RETAIL SALES`, `RETAIL TRANSFERS`, and `WAREHOUSE SALES`—represent physical unit/case volume movements, not dollar revenues. There are no price, cost, or wholesale tariff columns in the source data.
> 
> Fabricating a price multiplier or assuming arbitrary margins would violate business reality and produce hallucinations. Similarly, calculating inventory turnover requires snapshot inventory balances on hand, whereas this dataset captures transactional movement. I deliberately framed the project around **physical supply chain and distribution analytics**, which provided genuine, defensible operational insights."

---

## 3. SQL Architecture & Troubleshooting

### Q: "What was a specific SQL challenge you solved during this project?"
**Answer**:
> "The initial SQL analysis suite drafted by a predecessor included a query that used the `QUALIFY` clause: `QUALIFY rank_in_year <= 3`. While modern cloud data warehouses like Snowflake, DuckDB, or BigQuery support `QUALIFY` to filter window function outputs, SQLite—including the active 3.50 release—does not support `QUALIFY` syntax and throws a syntax error.
> 
> I refactored Query 16 into a Common Table Expression (CTE) and subquery pattern:
> ```sql
> WITH yearly_item_type AS (
>     SELECT year, item_type, SUM(retail_sales) AS total_retail_sales
>     FROM sales
>     GROUP BY year, item_type
> ),
> ranked_item_types AS (
>     SELECT year, item_type, ROUND(total_retail_sales, 2) AS total_retail_sales,
>            RANK() OVER (PARTITION BY year ORDER BY total_retail_sales DESC) AS rank_in_year
>     FROM yearly_item_type
> )
> SELECT year, item_type, total_retail_sales, rank_in_year
> FROM ranked_item_types
> WHERE rank_in_year <= 3
> ORDER BY year, rank_in_year;
> ```
> This achieved full cross-engine compatibility with standard ANSI/SQLite execution while preserving clean readability."

---

## 4. Verification & Testing

### Q: "How did you ensure that your Python pipeline and SQL analytics produced reliable, identical numbers?"
**Answer**:
> "I built an automated 25-test suite using Python's `unittest` framework, highlighted by a dedicated cross-engine reconciliation module (`test_python_sql_consistency.py`).
> 
> The test independently queries the SQLite database via `sqlite3` and executes vector aggregations in Pandas against `cleaned_sales.csv`. It asserts that total retail sales (`2,160,899.37`), total warehouse sales (`7,781,756.28`), total retail transfers (`2,133,968.63`), category aggregates, and top supplier rankings reconcile within a strict tolerance (`delta < 0.05`). Both engines agreed with `0.0000` discrepancy, proving complete pipeline reproducibility."

---

## 5. Strategic & Business Insights

### Q: "What were the most significant operational findings from this analysis?"
**Answer**:
> "Three major findings stood out:
> 1. **Wholesale-Heavy Operational Model**: Out of 12.08M total units moved, **64.4%** moved through warehouse wholesale to commercial licensees, while store retail represented only **17.9%**.
> 2. **Category Channel Disparity**: Beer represents **83.9% of all warehouse shipments**, driven by restaurants and bars, but only 26.6% of retail store sales. Conversely, distilled spirits (Liquor) dominate retail sales at **37.2%** of volume, but account for only 1.2% of warehouse sales due to county retail exclusivity.
> 3. **High Supplier Dependency (Pareto 80/20)**: Although there are 397 suppliers, the top 10 drive **47.3%** and the top 20 drive **67.9%** of all retail volume. Supply chain SLA monitoring should focus heavily on these top 20 suppliers to protect the vast majority of volume."

---

## 6. Temporal Volatility & Anomaly Detection

### Q: "Did you identify any temporal anomalies or reporting irregularities?"
**Answer**:
> "Yes. When analyzing the date distribution across the 4 recorded years, I found that the dataset does not represent 48 continuous calendar months, but exactly **24 active reporting months** (7 in 2017, 2 in 2018, 11 in 2019, and 4 in 2020).
> 
> This meant raw annual sums were misleading without monthly normalization. Looking at comparable months, I observed strong seasonal holiday surges in December (+35.6% above baseline), followed by recurring January volume lows (~40% contraction). Crucially, in March 2020, retail store sales spiked to 109,411 units—the second-highest month in history—capturing consumer pantry-loading right before early pandemic lockdowns."
