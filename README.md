# Retail & Warehouse Sales Analytics

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/Database-SQLite%203-lightgrey.svg)](https://www.sqlite.org/)
[![Tests](https://img.shields.io/badge/Unit%20Tests-25%20Passed-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()

An end-to-end data engineering, analytics, and business intelligence project analyzing **307,642 multi-channel alcohol sales and logistics records** (representing **12.08 million units of physical volume movement**) across retail stores and wholesale warehouse distribution.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Business Problem & Context](#business-problem--context)
- [Core Objectives](#core-objectives)
- [Dataset Summary](#dataset-summary)
- [Technologies Used](#technologies-used)
- [Project Architecture](#project-architecture)
- [Data Cleaning & Validation](#data-cleaning--validation)
- [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
- [Headline Business KPIs](#headline-business-kpis)
- [SQL Analytics Suite](#sql-analytics-suite)
- [Cross-Engine Reconciliation (Python vs SQL)](#cross-engine-reconciliation-python-vs-sql)
- [Power BI Dashboard Specification](#power-bi-dashboard-specification)
- [Key Business Insights](#key-business-insights)
- [Automated Testing Suite](#automated-testing-suite)
- [Known Limitations](#known-limitations)
- [Future Improvements](#future-improvements)
- [How to Run (Quickstart)](#how-to-run-quickstart)

---

## Project Overview

This repository demonstrates a production-grade analytics workflow that transforms raw, unindexed transactional data into a fully tested analytics warehouse, publication-quality visualizations, and an executive Business Intelligence dashboard.

> [!IMPORTANT]
> **Physical Volume Semantics**: All metrics in this project represent **physical movement/sales volume (cases and units)**, not monetary revenue. In accordance with data integrity principles, no fictional prices, margins, or profits have been invented.

---

## Business Problem & Context

The dataset reflects public beverage control logistics (Montgomery County Department of Liquor Control), where a central warehouse manages both county-operated retail liquor stores and wholesale distribution to licensed commercial entities (restaurants, bars, private retailers).

Key business challenges addressed:
1. **Channel Disparity**: How does product mix differ between store walk-in consumers and commercial wholesale licensees?
2. **Supplier Concentration**: How heavily does the operation rely on top conglomerate suppliers (Pareto risk)?
3. **Replenishment Coupling**: Does store replenishment (transfers) accurately track retail customer demand?
4. **Demand Shocks & Seasonality**: How do holiday demand surges (December) and external shocks (early COVID-19 panic buying) impact inventory movement?

---

## Core Objectives

- **Automated Data Pipeline**: Clean, validate, and impute raw transactional records using Pandas and NumPy.
- **SQL Warehouse Architecture**: Load 307K+ records into an indexed SQLite database and execute 18 advanced queries using CTEs and window functions (`RANK`, `LAG`, running sums).
- **Cross-Engine Verification**: Programmatically prove 100% numerical consistency between Python dataframes and SQL database queries.
- **Publication Visualizations**: Generate 8 high-resolution (300 DPI) charts for reporting.
- **Enterprise Power BI Model**: Formulate star-adjacent data models, custom calendar dimensions, and 14 production DAX measures.
- **Automated Testing**: Enforce a 25-test automated testing suite (`unittest`).

---

## Dataset Summary

- **Source**: [Kaggle - Retail Sales Data Set of Alcohol and Liquor](https://www.kaggle.com/datasets/fatemehmohammadinia/retail-sales-data-set-of-alcohol-and-liquor)
- **Raw Row Count**: 307,645 records
- **Cleaned Row Count**: 307,642 records (3 records lacking retail sales and supplier were dropped)
- **Time Horizon**: 2017 – 2020 (24 active reporting calendar months)
- **Catalog Depth**: 34,820 SKUs across 397 Suppliers

| Column | Type | Semantic Meaning |
|---|---|---|
| `YEAR` | Integer | Transaction calendar year (2017–2020) |
| `MONTH` | Integer | Transaction calendar month (1–12) |
| `SUPPLIER` | String | Beverage vendor / manufacturer |
| `ITEM CODE` | String | Unique product SKU identifier |
| `ITEM DESCRIPTION` | String | Product name and bottle package size |
| `ITEM TYPE` | String | Category (`LIQUOR`, `WINE`, `BEER`, etc.) |
| `RETAIL SALES` | Float | Physical units sold through retail stores |
| `RETAIL TRANSFERS` | Float | Physical units transferred from warehouse to retail |
| `WAREHOUSE SALES` | Float | Physical units shipped directly to commercial licensees |

---

## Technologies Used

- **Language**: Python 3.10+
- **Data Engineering & Manipulation**: Pandas, NumPy
- **Relational Database**: SQLite 3 (ANSI SQL, CTEs, Window Functions, B-Tree Indexes)
- **Data Visualization**: Matplotlib, Seaborn
- **Automated Testing**: Python `unittest` framework
- **Business Intelligence**: Power BI Desktop (DAX, Power Query, Star Schema Modeling)

---

## Project Architecture

```
Retail-Sales-Analytics/
│
├── data/
│   ├── Warehouse_and_Retail_Sales.csv   # Raw source dataset (307,645 rows)
│   └── cleaned_sales.csv                # Validated clean dataset (307,642 rows)
│
├── python/
│   ├── data_cleaning.py                 # Pipeline: validation, null imputation, type casting
│   ├── eda.py                           # Statistical profiling, returns analysis, correlations
│   ├── analysis.py                      # Core KPIs, Pareto distributions, temporal aggregations
│   └── generate_charts.py               # Generates 8 publication-grade charts (300 DPI)
│
├── SQL/
│   ├── schema.sql                       # DDL: table definition and 4 performance B-tree indexes
│   ├── load_data.py                     # Streaming batch ETL loader and query executor
│   ├── database.db                      # Fully populated SQLite warehouse database
│   ├── analysis.sql                     # Full SQL analysis suite (18 queries)
│   ├── queries/                         # 18 standalone executable SQL files
│   └── README.md                        # Schema and query catalog documentation
│
├── Dashboard/
│   ├── monthly_retail_sales.png         # Monthly Retail Sales Trend (Volume)
│   ├── sales_by_item_type.png          # Retail Sales Volume by Item Type
│   ├── top_suppliers.png               # Top 10 Suppliers by Retail Volume
│   ├── top_products.png                # Top 10 Products by Retail Volume
│   ├── yearly_sales_comparison.png     # Yearly Retail vs Warehouse vs Transfers
│   ├── retail_transfers_trend.png      # Monthly Retail Transfers Trend
│   ├── retail_vs_warehouse_comparison.png # Channel Movement Comparison & Ratio
│   └── supplier_contribution.png       # Pareto Supplier Contribution & Cumulative Share
│
├── PowerBI/
│   ├── Dashboard_Specification.md       # Canvas layout, grids, and interaction model
│   ├── Data_Model.md                    # Star-adjacent relational model and Calendar DAX
│   ├── DAX_Measures.md                  # 14 fully formulated production DAX measures
│   ├── Visuals.md                       # Visual-by-visual configuration and field mappings
│   └── Build_Instructions.md            # 15-minute quickstart build guide
│
├── tests/
│   ├── test_data.py                     # Schema validation, missing values, datatypes, bounds
│   ├── test_analysis.py                 # Business KPIs, Pareto logic, temporal groupings
│   ├── test_sql.py                      # DB presence, record count, index check, 18 queries
│   ├── test_python_sql_consistency.py   # Cross-engine reconciliation (Python vs SQL totals)
│   └── README.md                        # Test execution instructions
│
├── docs/
│   ├── PROJECT_STATUS.md                # Lifecycle status, completed deliverables, audit trail
│   ├── DATA_QUALITY_REPORT.md           # Formal profiling, null handling, returns semantics
│   ├── BUSINESS_INSIGHTS.md             # Data-backed operational findings & strategic takeaways
│   ├── resume_bullets.md                # Tailored metric-backed resume bullet points
│   ├── project_summary.md               # Executive summary for recruiters and portfolio
│   └── interview_questions.md           # Technical & business Q&A preparation
│
├── README.md                            # Main project documentation
└── requirements.txt                     # Pinned minimal dependencies
```

---

## Data Cleaning & Validation

The pipeline (`python/data_cleaning.py`) applies strict business rules:
1. **Target Metric Nulls**: 3 records where `RETAIL SALES` was NaN were dropped (these also lacked supplier data).
2. **Supplier Imputation**: 164 records with missing `SUPPLIER` were imputed with `'Unknown'`.
3. **Category Imputation**: Exactly 1 record (row 96129, Barolo wine) with null `ITEM TYPE` was imputed with `'Unknown'`.
4. **Negative Volume Semantics**: Negative values (113 retail, 1,016 transfers, 716 warehouse) were **preserved** as legitimate customer returns, keg deposit adjustments, and reverse transfers.
5. **Type Casting & Normalization**: Stripped text whitespace, coerced numeric fields, and rounded float values to 2 decimal places.

---

## Headline Business KPIs

| Metric | Exact Value | Operational Context |
|---|---|---|
| **Total Movement Volume** | **12,076,624.28 units** | Aggregate supply chain logistics volume |
| **Wholesale Warehouse Sales** | **7,781,756.28 units** | 64.44% of total movement |
| **Retail Store Sales** | **2,160,899.37 units** | 17.89% of total movement |
| **Retail Replenishment Transfers**| **2,133,968.63 units** | 17.67% of total movement |
| **Retail-to-Warehouse Ratio** | **0.2777** | ~1 retail unit for every 3.6 warehouse units |
| **Average Retail Sales/Record** | **7.0241 units** | Average volume per line-item transaction |
| **Replenishment Correlation** | **0.9601** | Pearson correlation between retail sales and transfers |

---

## SQL Analytics Suite

The SQL layer (`SQL/`) provides a suite of 18 analytical queries covering:
- **Core Aggregations**: Total volumes, category distributions, supplier rankings, product rankings.
- **Time Intelligence**: Monthly rollups, annual channel breakdowns, Year-over-Year volume growth via `LAG()`.
- **Pareto & Market Share**: Supplier cumulative percentage via window `SUM() OVER (...)`.
- **Window Partitions**: Annual category leadership via `RANK() OVER (PARTITION BY year ...)`.
- **Movement Classification**: Multi-condition `CASE WHEN` classifying categories into *Retail Dominant*, *Warehouse Dominant*, or *Channel Only*.

---

## Cross-Engine Reconciliation (Python vs SQL)

To guarantee that calculations are robust and reproducible, `tests/test_python_sql_consistency.py` independently computes totals in Pandas and queries the SQLite database:

```
[Cross-Engine Reconciliation Results]
----------------------------------------------------------------------
Retail Sales Volume     : Python = 2,160,899.37 | SQL = 2,160,899.37 | Diff = 0.0000
Warehouse Sales Volume  : Python = 7,781,756.28 | SQL = 7,781,756.28 | Diff = 0.0000
Retail Transfers Volume : Python = 2,133,968.63 | SQL = 2,133,968.63 | Diff = 0.0000
Item Type Aggregates    : All 9 Categories match exactly (Diff < 0.01)
Top 5 Suppliers Volume  : All 5 Suppliers match exactly (Diff < 0.01)
----------------------------------------------------------------------
Reconciliation Status: 100% MATCH
```

---

## Power BI Dashboard Specification

A complete 2-page dashboard architecture is fully detailed in `PowerBI/`:
- **Page 1: Executive Overview**: 4 headline KPI cards, monthly retail trend line with peak callout, yearly channel column chart, item type horizontal bars, and top 10 suppliers.
- **Page 2: Product & Supplier Analysis**: Top 10 SKUs, Pareto supplier combination chart (bar volume + cumulative % line), supplier catalog breadth scatter plot, and product hierarchy matrix.
- **14 Production DAX Measures**: Includes time intelligence (`SAMEPERIODLASTYEAR`), running Pareto sums, and error-guarded ratios (`DIVIDE`).

---

## Key Business Insights

1. **Wholesale Dominance**: The operation is primarily wholesale-driven (**64.4%** of volume). Retail accounts for only **17.9%**.
2. **Extreme Category Channel Divergence**:
   - **Beer** drives **83.9%** of warehouse volume, but only 26.6% of retail sales.
   - **Liquor** drives **37.2%** of retail sales, but only 1.2% of warehouse shipments (due to county retail exclusivity).
3. **Supplier Pareto Distribution**: The top 10 suppliers account for **47.3%** of retail volume; the top 20 account for **67.9%**.
4. **Replenishment Synchronization**: Retail sales and inter-facility transfers correlate at **0.9601**, demonstrating demand-driven warehouse replenishment.
5. **Seasonal Shocks**: December represents the annual peak (**131,634 units**, +35.6% above baseline), while March 2020 experienced an unprecedented surge (**109,411 units**) driven by COVID-19 consumer pantry-loading.

---

## Automated Testing Suite

All **25 automated tests** run cleanly via Python's standard `unittest` framework:

```powershell
python -m unittest discover tests -v
```

```
Ran 25 tests in 8.975s

OK
```

---

## Known Limitations

1. **Temporal Gaps**: The dataset covers 24 discrete months across 4 calendar years (e.g., 2018 has 2 months, 2020 has 4 months). Annual comparisons require normalization.
2. **Absence of Monetary Data**: Prices, margins, and financial costs are absent from the dataset. All metrics reflect physical volume movement.
3. **Snapshot Inventories**: Beginning/ending store inventory balances are not recorded; inventory turns cannot be directly derived.

---

## Future Improvements

- **Forecasting Module**: Implement seasonal ARIMA / Prophet time-series models on continuous monthly spans to forecast store replenishment.
- **Reorder Point Optimization**: Estimate safety stock levels and stockout risks based on transfer latency and demand variance.
- **Streamlit Interactive App**: Build a lightweight Python web application to complement the Power BI specification.

---

## How to Run (Quickstart)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Data Cleaning Pipeline
```bash
python python/data_cleaning.py
```

### 3. Initialize SQLite Database & Load Data
```bash
python SQL/load_data.py
```

### 4. Execute Analysis & Generate Visualizations
```bash
python python/analysis.py
python python/generate_charts.py
```

### 5. Run the Automated Test Suite
```bash
python -m unittest discover tests -v
```
