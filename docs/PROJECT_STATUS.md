# Project Status: Retail & Warehouse Sales Analytics

## Completion Percentage: 100%

## Current Phase: Complete, Tested, Verified, and GitHub/Resume-Ready

---

## Completed Work

1. **Root Directory Cleanup**:
   - Removed untracked loose testing images (`Figure_1.png`, `monthly_sales.png`).
2. **Data Engineering & Cleaning Pipeline**:
   - Built modular `python/data_cleaning.py`.
   - Identified and handled nulls: dropped 3 rows missing `RETAIL SALES` and supplier; imputed 164 missing suppliers with `'Unknown'`; imputed 1 missing item type (Barolo wine) with `'Unknown'`.
   - Preserved negative values across retail sales (113 records), transfers (1,016 records), and warehouse sales (716 records) as legitimate operational returns and reversals.
   - Generated persistent, validated dataset `data/cleaned_sales.csv` (307,642 rows).
3. **Exploratory Data Analysis (EDA)**:
   - Built `python/eda.py` performing distribution profiling, skewness/kurtosis calculation, zero-volume analysis, channel correlations (0.9601 between retail sales and transfers), and temporal mapping across 24 discrete active months.
4. **Python Business Analysis Engine**:
   - Refactored `python/analysis.py` into a clean, modular calculation suite for headline volume KPIs, item type shares, Pareto supplier rankings, product volumes, monthly/yearly aggregations, and peak/trough analyses.
5. **Dashboard Visualizations**:
   - Built `python/generate_charts.py` producing all 8 required publication-grade, 300 DPI visualizations in `Dashboard/`:
     1. `monthly_retail_sales.png`
     2. `sales_by_item_type.png`
     3. `top_suppliers.png`
     4. `top_products.png`
     5. `yearly_sales_comparison.png`
     6. `retail_transfers_trend.png`
     7. `retail_vs_warehouse_comparison.png`
     8. `supplier_contribution.png`
6. **SQL Analytics Layer & SQLite Warehouse**:
   - Verified active SQLite version (`3.50.4`).
   - Fixed Query 16 syntax incompatibility in `SQL/analysis.sql` (replaced unsupported `QUALIFY` clause with ANSI-compliant CTE + `WHERE` filter).
   - Built `SQL/load_data.py` to stream `data/cleaned_sales.csv` into `SQL/database.db`, verify row counts (307,642), and validate 4 performance B-tree indexes.
   - Created `SQL/queries/` containing all 18 individual, standalone executable `.sql` queries.
   - Authored comprehensive `SQL/README.md`.
7. **Cross-Engine Reconciliation (Python vs SQL)**:
   - Built `tests/test_python_sql_consistency.py` validating that Python and SQLite calculate identical sums down to the decimal place (`Diff = 0.0000` across 2.16M retail sales, 7.78M warehouse sales, and 2.13M transfers).
8. **Automated Testing Suite**:
   - Built 4 test modules in `tests/`: `test_data.py`, `test_analysis.py`, `test_sql.py`, `test_python_sql_consistency.py`, and `tests/README.md`.
   - Executed full test suite: **25 tests run, 25 tests passed (100% pass rate)**.
9. **Power BI Package**:
   - Built complete 5-file specification suite in `PowerBI/`: `Dashboard_Specification.md`, `Data_Model.md`, `DAX_Measures.md`, `Visuals.md`, `Build_Instructions.md`.
   - Transparently stated environment constraints regarding binary `.pbix` creation without fabricating files.
10. **Documentation & Career Deliverables**:
    - Authored `docs/DATA_QUALITY_REPORT.md` (full profiling and audit trail).
    - Authored `docs/BUSINESS_INSIGHTS.md` (data-backed operational findings).
    - Authored `docs/resume_bullets.md` (4 tailored, metric-backed bullet options).
    - Authored `docs/project_summary.md` (executive portfolio summary).
    - Authored `docs/interview_questions.md` (7 technical & business interview prep scenarios).
    - Created `requirements.txt` with minimal dependencies.
    - Authored production-grade root `README.md`.

---

## Files Created

- `data/cleaned_sales.csv`
- `python/data_cleaning.py`
- `python/eda.py`
- `python/generate_charts.py`
- `Dashboard/retail_transfers_trend.png`
- `Dashboard/retail_vs_warehouse_comparison.png`
- `Dashboard/supplier_contribution.png`
- `Dashboard/top_products.png`
- `SQL/database.db`
- `SQL/load_data.py`
- `SQL/README.md`
- `SQL/queries/01_total_retail_sales_volume.sql` through `18_retail_vs_warehouse_movement.sql` (18 files)
- `tests/test_data.py`
- `tests/test_analysis.py`
- `tests/test_sql.py`
- `tests/test_python_sql_consistency.py`
- `tests/README.md`
- `PowerBI/Dashboard_Specification.md`
- `PowerBI/Data_Model.md`
- `PowerBI/DAX_Measures.md`
- `PowerBI/Visuals.md`
- `PowerBI/Build_Instructions.md`
- `docs/DATA_QUALITY_REPORT.md`
- `docs/BUSINESS_INSIGHTS.md`
- `docs/resume_bullets.md`
- `docs/project_summary.md`
- `docs/interview_questions.md`
- `docs/PROJECT_STATUS.md`
- `README.md`
- `requirements.txt`

---

## Files Modified

- `python/analysis.py` (refactored from monolith to clean modular analytical pipeline)
- `SQL/analysis.sql` (fixed Query 16 `QUALIFY` incompatibility for SQLite)
- `Dashboard/monthly_retail_sales.png` (regenerated at 300 DPI with peak annotations)
- `Dashboard/sales_by_item_type.png` (regenerated at 300 DPI with percentage labels)
- `Dashboard/top_suppliers.png` (regenerated at 300 DPI with clean bar formatting)
- `Dashboard/yearly_sales_comparison.png` (regenerated at 300 DPI with 3-channel grouped bars)

---

## Tests Run, Passed, and Failed

- **Total Tests Run**: 25
- **Tests Passed**: 25
- **Tests Failed**: 0
- **Test Errors**: 0
- **Pass Rate**: 100%

---

## Current Errors

- **None**. The codebase runs cleanly with zero syntax errors, zero runtime exceptions, and zero warnings.

---

## Current Working State

The project is completely self-contained, reproducible, fully documented, and ready for GitHub and technical portfolio review.

---

## Important Dataset Findings

1. **Total Logistics Volume**: 12,076,624.28 physical units/cases across all channels.
2. **Channel Breakdown**: Wholesale warehouse distribution represents 64.44% (7,781,756.28 units); retail store sales represent 17.89% (2,160,899.37 units); store replenishment transfers represent 17.67% (2,133,968.63 units).
3. **Channel Ratio**: Retail-to-Warehouse ratio is 0.2777 (~1 retail unit sold for every 3.6 warehouse units shipped).
4. **Replenishment Synchronization**: Retail sales and retail transfers correlate at 0.9601 (Pearson r), indicating tight warehouse-to-store pull-replenishment.
5. **Category Channel Disparity**:
   - Beer represents 83.88% of warehouse volume, but only 26.57% of retail sales.
   - Liquor represents 37.15% of retail sales, but only 1.22% of warehouse volume.
6. **Supplier Concentration**: Top 10 suppliers account for 47.30% of retail sales; top 20 account for 67.87% (Pareto distribution).
7. **Top SKU**: Tito's Handmade Vodka 1.75L is the #1 retail product (27,580.50 units, 1.28% of total store volume).
8. **Temporal Characteristics**: Dataset spans 24 active months across 2017 (7 mos), 2018 (2 mos), 2019 (11 mos), and 2020 (4 mos). Retail peaks in December (+35.6% above baseline); March 2020 exhibited an unprecedented spike (109,411 units) driven by early COVID-19 consumer pantry-loading.

---

## Important Technical Decisions

1. **Volume Semantics Enforced**: Strictly prohibited inventing financial revenue, prices, or margins.
2. **Negative Returns Preserved**: Negative values (returns/reversals) were retained to reflect true net physical movement.
3. **SQLite Query 16 Refactor**: Replaced DuckDB/Snowflake-style `QUALIFY` with standard CTE + `WHERE` filter for universal ANSI/SQLite execution.
4. **Cross-Engine Reconciliation**: Enforced automated numeric tolerance tests between Pandas and SQLite.

---

## Power BI Status

- Fully specified across 5 documentation files in `PowerBI/`.
- Ready for immediate drag-and-drop assembly in Power BI Desktop in under 15 minutes.
- Explicitly stated that no native `.pbix` compiler exists in CLI to ensure complete transparency.

---

## Remaining Tasks

- None. All project requirements have been implemented and verified.

---

## Exact Next Steps (for User / Reviewer)

1. Clone or open `Retail-Sales-Analytics/`.
2. Inspect the GitHub `README.md`.
3. Review the high-resolution charts in `Dashboard/`.
4. Run the automated test suite to confirm end-to-end reproducibility.

---

## Commands to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run data cleaning pipeline
python python/data_cleaning.py

# 3. Run exploratory data analysis
python python/eda.py

# 4. Run business KPI analysis
python python/analysis.py

# 5. Generate high-resolution charts
python python/generate_charts.py

# 6. Initialize SQLite database & load records
python SQL/load_data.py

# 7. Run full automated test suite
python -m unittest discover tests -v

# 8. Run cross-engine reconciliation test
python tests/test_python_sql_consistency.py
```
