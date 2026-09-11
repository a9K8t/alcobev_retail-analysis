# Data Quality & Profiling Report: Retail & Warehouse Sales Analytics

## 1. Executive Summary

This report provides a formal audit of data quality, data integrity, cleaning transformations, and validation results for the **Retail & Warehouse Sales** dataset (originating from Montgomery County Department of Liquor Control alcoholic beverage distributions).

---

## 2. Dataset Dimensions & Volume

| Metric | Raw Dataset | Cleaned Dataset | Variance / Action |
|---|---|---|---|
| **Total Row Count** | 307,645 | 307,642 | -3 rows (0.00098% dropped) |
| **Total Columns** | 9 | 9 | Preserved schema |
| **Memory Footprint** | ~21.1 MB (disk: ~25.8 MB) | ~21.1 MB (disk: ~27.0 MB) | Cast to optimized datatypes |
| **Total Retail Volume** | 2,160,899.37 units | 2,160,899.37 units | Unchanged |
| **Total Warehouse Volume** | 7,781,756.28 units | 7,781,756.28 units | Unchanged |
| **Total Transfers Volume** | 2,133,968.63 units | 2,133,968.63 units | Unchanged |

---

## 3. Missing Value Audit & Imputation Strategy

| Column | Missing in Raw | % Missing | Remediation Strategy | Post-Clean Missing |
|---|---|---|---|---|
| `YEAR` | 0 | 0.00% | None needed | 0 |
| `MONTH` | 0 | 0.00% | None needed | 0 |
| `SUPPLIER` | 167 | 0.054% | Imputed with `"Unknown"`. (3 were in rows with missing sales; 164 imputed). | 0 |
| `ITEM CODE` | 0 | 0.00% | None needed | 0 |
| `ITEM DESCRIPTION` | 0 | 0.00% | None needed | 0 |
| `ITEM TYPE` | 1 | 0.0003% | Imputed with `"Unknown"` (Row 96129: "FONTANAFREDDA BAROLO SILVER LABEL 750 ML"). | 0 |
| `RETAIL SALES` | 3 | 0.00098% | **Dropped**. Rows 18390, 299150, 300935 lacked both retail sales volume and supplier data. | 0 |
| `RETAIL TRANSFERS` | 0 | 0.00% | None needed | 0 |
| `WAREHOUSE SALES` | 0 | 0.00% | None needed | 0 |

---

## 4. Duplicate Records

- **Full Row Duplicates**: `0` duplicate rows detected across all 9 columns.
- **Granularity Validation**: Each row represents an aggregated monthly SKU-level movement record per supplier and store/warehouse channel. No unintended duplicate keys exist.

---

## 5. Negative Values & Transaction Semantics

Analysis identified negative numeric values across volume channels. Rather than being data corruption, these reflect legitimate operational returns, pallet credits, and transfer reversals:

| Metric | Negative Record Count | % of Dataset | Aggregate Volume | Range (Min Value) | Operational Interpretation |
|---|---|---|---|---|---|
| **RETAIL SALES** | 113 | 0.037% | -43.37 units | -6.49 units | Customer returns to retail stores |
| **RETAIL TRANSFERS** | 1,016 | 0.330% | -752.97 units | -38.49 units | Reverse logistics (store-to-warehouse stock returns) |
| **WAREHOUSE SALES** | 716 | 0.233% | -143,752.59 units | -7,800.00 units | Wholesale distributor returns, keg deposits, and packaging dunnage credits |

> [!NOTE]
> Negative transactions were intentionally **preserved** in both Python and SQL layers to maintain true net movement volume.

---

## 6. Temporal Sparsity & Reporting Gaps

Temporal inspection revealed that the dataset is **not** a continuous 48-month time series. It contains **24 distinct reporting months**:
- **2017**: 7 months (June through December) — 96,284 records
- **2018**: 2 months (January and February only) — 26,445 records
- **2019**: 11 months (January through November; December omitted) — 138,638 records
- **2020**: 4 months (January, March, July, September) — 46,275 records

### Analytical Impact
Direct comparisons of annual totals (e.g., 2017 sum vs 2018 sum) are inherently biased by the count of active months. All annualized analyses must normalize by active months or evaluate month-over-month comparable periods.

---

## 7. Automated Validation Results

All 25 automated tests in `tests/` passed:
- `test_data.py`: Schema validation, null checks, type enforcement, and domain range assertions passed.
- `test_python_sql_consistency.py`: Reconciled Python totals against SQLite database with zero variance (`Diff = 0.0000`).
