# Test Suite: Retail & Warehouse Sales Analytics

This test suite verifies data integrity, analysis logic, SQLite database stability, cross-engine consistency, and chart generation.

## Test Directory Structure

```
tests/
├── test_data.py                    # Schema validation, missing values, datatypes, bounds
├── test_analysis.py                # Business KPIs, Pareto logic, temporal groupings, chart existence
├── test_sql.py                     # SQLite database presence, record count, index check, all 18 SQL queries
├── test_python_sql_consistency.py  # Cross-engine reconciliation (Python vs SQL totals)
└── README.md                       # Test instructions and documentation
```

## How to Run All Tests

Run all unit tests across the entire suite with verbose reporting:

```powershell
python -m unittest discover tests -v
```

## How to Run Individual Test Modules

### 1. Data Integrity Tests
```powershell
python -m unittest tests/test_data.py -v
```
Validates:
- Raw and cleaned file presence
- Exact 307,642 row count
- Zero null values
- Valid year range (2017-2020) and month range (1-12)

### 2. Analysis & KPI Tests
```powershell
python -m unittest tests/test_analysis.py -v
```
Validates:
- Non-negative KPI volumes
- Top item types, top suppliers, and top products
- 24 chronological monthly periods
- All 8 high-resolution 300 DPI chart images in `Dashboard/`

### 3. SQL Database & Query Tests
```powershell
python -m unittest tests/test_sql.py -v
```
Validates:
- `SQL/database.db` presence
- `sales` table record count (307,642)
- 4 performance indexes
- Clean syntax execution of all 18 individual queries in `SQL/queries/`

### 4. Cross-Engine Consistency (Python vs SQL)
```powershell
python -m unittest tests/test_python_sql_consistency.py -v
```
Validates:
- Total Retail Sales reconciliation within delta < 0.05
- Total Warehouse Sales reconciliation within delta < 0.05
- Total Retail Transfers reconciliation within delta < 0.05
- Item Type aggregates reconciliation
- Top 5 supplier volumes reconciliation
