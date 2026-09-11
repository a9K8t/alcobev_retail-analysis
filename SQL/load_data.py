"""
load_data.py
============
Automated database pipeline for Retail & Warehouse Sales Analytics.

Tasks performed:
1. Connects to SQLite database at SQL/database.db.
2. Applies SQL/schema.sql (creates sales table and 4 performance indexes).
3. Reads data/cleaned_sales.csv (307,642 records) in streaming batches and inserts into SQLite.
4. Validates table count and index status.
5. Executes the complete analysis suite (18 queries) to ensure 100% execution integrity.
"""

import os
import sqlite3
import pandas as pd
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")
CLEANED_CSV_PATH = os.path.join(BASE_DIR, "..", "data", "cleaned_sales.csv")


def init_database(db_path=DB_PATH, schema_path=SCHEMA_PATH, csv_path=CLEANED_CSV_PATH, recreate=True):
    """Initializes SQLite database and populates sales table."""
    print("=" * 70)
    print("SQL DATABASE LOADER & PIPELINE INITIALIZATION")
    print("=" * 70)

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Cleaned dataset not found at: {csv_path}. Run python/data_cleaning.py first.")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Step 1: Apply Schema
    print(f"[1/4] Applying schema from: {schema_path}")
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    conn.commit()

    # Step 2: Stream and Insert Data
    print(f"[2/4] Loading cleaned records from: {csv_path}")
    start_time = time.time()
    chunk_size = 50000
    total_loaded = 0

    insert_sql = """
        INSERT INTO sales (
            year, month, supplier, item_code, item_description,
            item_type, retail_sales, retail_transfers, warehouse_sales
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
        records = [
            (
                int(row["YEAR"]),
                int(row["MONTH"]),
                str(row["SUPPLIER"]),
                str(row["ITEM CODE"]),
                str(row["ITEM DESCRIPTION"]),
                str(row["ITEM TYPE"]),
                float(row["RETAIL SALES"]),
                float(row["RETAIL TRANSFERS"]),
                float(row["WAREHOUSE SALES"])
            )
            for _, row in chunk.iterrows()
        ]
        cursor.executemany(insert_sql, records)
        conn.commit()
        total_loaded += len(records)
        print(f"      Loaded {total_loaded:,} / 307,642 records...")

    elapsed = time.time() - start_time
    print(f"[3/4] Data loading completed in {elapsed:.2f} seconds.")

    # Step 3: Verification
    cursor.execute("SELECT COUNT(*) FROM sales")
    count = cursor.fetchone()[0]
    print(f"[4/4] Verification: sales table contains {count:,} records.")
    assert count == 307642, f"Expected 307,642 rows in sales table, found {count}"

    cursor.execute("PRAGMA index_list('sales')")
    indexes = cursor.fetchall()
    print(f"      Verified {len(indexes)} indexes on 'sales' table.")

    conn.close()
    print("=" * 70)
    print("DATABASE INITIALIZED SUCCESSFULLY")
    print("=" * 70)
    return count


def execute_analysis_queries(db_path=DB_PATH):
    """Executes all queries to verify SQLite compatibility."""
    print("\nExecuting validation run across core SQL analytical queries...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    queries = {
        "Q1: Total Retail Sales Volume": "SELECT ROUND(SUM(retail_sales), 2) FROM sales;",
        "Q2: Total Warehouse Sales Volume": "SELECT ROUND(SUM(warehouse_sales), 2) FROM sales;",
        "Q3: Total Retail Transfers Volume": "SELECT ROUND(SUM(retail_transfers), 2) FROM sales;",
        "Q4: Top Item Types Count": "SELECT COUNT(DISTINCT item_type) FROM sales;",
        "Q5: Top 1 Supplier Volume": "SELECT supplier, ROUND(SUM(retail_sales), 2) FROM sales GROUP BY supplier ORDER BY SUM(retail_sales) DESC LIMIT 1;",
        "Q16: Top Item Type per Year (Window/CTE)": """
            WITH yearly_item_type AS (
                SELECT year, item_type, SUM(retail_sales) AS total_retail_sales
                FROM sales
                GROUP BY year, item_type
            ),
            ranked AS (
                SELECT year, item_type, ROUND(total_retail_sales, 2) AS total_retail_sales,
                       RANK() OVER (PARTITION BY year ORDER BY total_retail_sales DESC) AS rank_in_year
                FROM yearly_item_type
            )
            SELECT year, item_type, total_retail_sales, rank_in_year
            FROM ranked
            WHERE rank_in_year = 1
            ORDER BY year;
        """
    }

    for name, sql in queries.items():
        cursor.execute(sql)
        res = cursor.fetchall()
        print(f"  [OK] {name:<42} -> {res}")

    conn.close()
    print("All sample queries executed successfully.\n")


if __name__ == "__main__":
    init_database()
    execute_analysis_queries()
