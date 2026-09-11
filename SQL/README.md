# SQL Analytics Layer: Retail & Warehouse Sales

This directory contains the database definition, automated ETL loading pipeline, and complete analytical SQL suite for the **Retail & Warehouse Sales Analytics** project.

## Architecture

- **Database Engine**: SQLite 3 (self-contained, serverless)
- **Database File**: `SQL/database.db`
- **Schema**: `SQL/schema.sql` (single fact-style table `sales` with 10 columns and 4 indexing strategies)
- **Loader**: `SQL/load_data.py` (streams `data/cleaned_sales.csv` in chunks, validates row counts, and verifies query execution)
- **Master SQL Suite**: `SQL/analysis.sql` (all 18 queries in one runnable script)
- **Modular Query Catalog**: `SQL/queries/` (18 individual `.sql` files for standalone execution)

---

## Schema Definition

```sql
CREATE TABLE sales (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    year              INTEGER NOT NULL,
    month             INTEGER NOT NULL,
    supplier          TEXT NOT NULL,
    item_code         TEXT NOT NULL,
    item_description  TEXT NOT NULL,
    item_type         TEXT NOT NULL,
    retail_sales      REAL NOT NULL,
    retail_transfers  REAL NOT NULL,
    warehouse_sales   REAL NOT NULL
);
```

### Performance Indexes

To accelerate common aggregation and filtering workloads, four B-tree indexes are defined:
1. `idx_sales_year_month` on `(year, month)` — Optimizes monthly and yearly temporal rollups.
2. `idx_sales_supplier` on `supplier` — Optimizes supplier Pareto and contribution queries.
3. `idx_sales_item_type` on `item_type` — Accelerates category volume breakdowns.
4. `idx_sales_item_desc` on `item_description` — Speeds up product catalog searches.

---

## Analytical Query Catalog

| Query File | Description | Key SQL Techniques |
|---|---|---|
| `01_total_retail_sales_volume.sql` | Total retail sales volume | `SUM`, `ROUND` |
| `02_total_warehouse_sales_volume.sql` | Total warehouse sales volume | `SUM`, `ROUND` |
| `03_total_retail_transfers_volume.sql` | Total retail transfers volume | `SUM`, `ROUND` |
| `04_sales_by_item_type.sql` | Volume and record count by item type | `GROUP BY`, `ORDER BY DESC` |
| `05_top_10_suppliers.sql` | Top 10 suppliers by retail volume | `GROUP BY`, `ORDER BY`, `LIMIT` |
| `06_top_10_products.sql` | Top 10 products by retail volume | `GROUP BY`, `ORDER BY`, `LIMIT` |
| `07_monthly_retail_sales.sql` | Chronological monthly retail sales | Multi-column `GROUP BY`, `ORDER BY` |
| `08_yearly_sales.sql` | Annual retail, warehouse, and transfer totals | `GROUP BY year` |
| `09_retail_to_warehouse_ratio.sql` | Annual retail-to-warehouse ratio | `CASE WHEN` division guard |
| `10_supplier_contribution.sql` | Supplier market share and cumulative % | CTE, `CROSS JOIN`, Window Function (`SUM() OVER`) |
| `11_product_contribution.sql` | Top 20 product market share | CTE, `CROSS JOIN` |
| `12_highest_performing_months.sql` | Top 5 peak volume months | `ORDER BY DESC LIMIT 5` |
| `13_lowest_performing_months.sql` | Bottom 5 trough volume months | `ORDER BY ASC LIMIT 5` |
| `14_lowest_performing_item_types.sql` | Bottom item types with noise threshold | `HAVING COUNT(*) >= 50` |
| `15_yoy_growth.sql` | Year-over-Year retail volume growth rate | CTE, Window Function (`LAG() OVER`) |
| `16_top_item_type_per_year.sql` | Top 3 item types per year | CTE, Window Function (`RANK() OVER PARTITION BY`) |
| `17_supplier_catalog_breadth.sql` | Supplier catalog breadth and diversification | `COUNT(DISTINCT item_type)`, `COUNT(DISTINCT item_description)` |
| `18_retail_vs_warehouse_movement.sql` | Retail vs warehouse channel classification | Multi-condition `CASE WHEN` classification |

---

## How to Run

### Automated Database Initialization & Verification
```bash
python SQL/load_data.py
```

### Running All Queries via Python
```python
import sqlite3

conn = sqlite3.connect("SQL/database.db")
cursor = conn.cursor()

with open("SQL/analysis.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

# Execute individual queries from SQL/queries/
for fname in sorted(os.listdir("SQL/queries")):
    with open(f"SQL/queries/{fname}") as qf:
        cursor.execute(qf.read())
        print(fname, cursor.fetchall())
```
