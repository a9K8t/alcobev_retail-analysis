# Project Summary: Retail & Warehouse Sales Analytics

## Overview

**Retail & Warehouse Sales Analytics** is an end-to-end data analytics and engineering project that processes, models, validates, and visualizes **307,642 multi-channel alcohol distribution records** (representing **12.08 million units/cases** of physical movement) between 2017 and 2020.

The project models the operational reality of public beverage control (Montgomery County Department of Liquor Control), where a central agency manages both county-operated retail liquor stores and wholesale distribution to licensed private establishments (restaurants, bars, independent beer/wine retailers).

---

## Core Problem & Business Context

In public and private liquor control logistics, balancing direct-to-consumer store retail with high-volume wholesale distribution is a complex challenge:
- How does product demand differ between retail consumer walk-ins and commercial licensee wholesale orders?
- How concentrated is supplier dependence across top global beverage conglomerates?
- Does retail store transfer activity match consumer sell-through, or is there excess inventory float?
- How volatile is seasonal demand across holiday surges, January troughs, and external shocks (such as COVID-19 panic buying)?

---

## Technical Stack & Architecture

```
[Raw CSV: 307,645 rows]
          │
          ▼
[python/data_cleaning.py] ──> [data/cleaned_sales.csv: 307,642 rows]
          │                                  │
          ├──────────────────────────────────┼──────────────────────────────────┐
          ▼                                  ▼                                  ▼
[python/analysis.py & eda.py]       [SQL/load_data.py]               [PowerBI/ Design Spec]
  - Headline KPIs                     - Applies schema.sql             - Data Model & Calendar
  - Pareto & Aggregations             - Streams CSV to SQLite          - 14 DAX Measures
  - 8 x 300 DPI Charts                - Generates database.db          - 2-Page Executive Dashboard
          │                           - Executes 18 SQL Queries                 │
          │                                  │                                  │
          └──────────────────┬───────────────┘                                  │
                             ▼                                                  │
                [Automated Test Suite: tests/] <────────────────────────────────┘
                  - test_data.py (Schema & Bounds)
                  - test_analysis.py (Logic & Charts)
                  - test_sql.py (DB & 18 Queries)
                  - test_python_sql_consistency.py (Cross-Engine Reconciliation)
                  - 25 Tests Ran / 25 Passed (0.0000 Diff)
```

---

## Key Metrics at a Glance

| Metric | Exact Calculated Value | Context |
|---|---|---|
| **Cleaned Dataset Records** | **307,642** | Filtered from 307,645 (3 null sales rows dropped) |
| **Total Movement Volume** | **12,076,624.28 units** | Aggregate logistics volume across all streams |
| **Wholesale Warehouse Sales** | **7,781,756.28 units** | 64.44% of total movement |
| **Retail Store Sales** | **2,160,899.37 units** | 17.89% of total movement |
| **Retail Replenishment Transfers** | **2,133,968.63 units** | 17.67% of total movement |
| **Retail-to-Warehouse Ratio** | **0.2777** | ~1 retail unit for every 3.6 warehouse units |
| **Replenishment Correlation** | **0.9601** | Pearson r between retail sales and transfers |
| **Distinct SKUs / Suppliers** | **34,820 SKUs / 397 Suppliers** | Massive catalog depth |
| **Supplier Concentration** | **47.30% (Top 10) / 67.87% (Top 20)** | Severe vendor concentration (Pareto principle) |
| **Top Volume SKU** | **Tito's Handmade Vodka 1.75L** | 27,580.50 retail units (1.28% of all retail volume) |
| **Test Suite Coverage** | **25 / 25 Tests Passed (100%)** | Zero numeric discrepancy between Python and SQL |

---

## Why This Project Stands Out

1. **Strict Semantic Integrity**: No fictional revenue or margin figures were fabricated; volume semantics (cases/units) are strictly preserved and documented.
2. **True Cross-Engine Verification**: Proves that SQL queries and Python data pipelines arrive at the exact same numbers down to the centesimal decimal place.
3. **Enterprise SQL Best Practices**: Avoids monolithic brittle queries; uses CTEs, window functions (`RANK`, `LAG`, running sums), and indexing strategies with tested SQLite compatibility.
4. **Production-Ready Code**: Modular structure, 25 unit tests, comprehensive data profiling, and complete Power BI specifications.
