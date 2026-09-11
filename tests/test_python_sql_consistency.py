"""
test_python_sql_consistency.py
==============================
Cross-Engine Validation Suite: Python (Pandas) vs SQL (SQLite).

Independently computes core volume metrics in both execution environments
and validates that results reconcile within a numerical tolerance (delta < 0.05).
"""

import os
import sqlite3
import unittest
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLEANED_CSV_PATH = os.path.join(BASE_DIR, "..", "data", "cleaned_sales.csv")
DB_PATH = os.path.join(BASE_DIR, "..", "SQL", "database.db")


class TestPythonSqlConsistency(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 1. Independent Python computation
        cls.df = pd.read_csv(CLEANED_CSV_PATH)
        cls.py_retail_total = float(cls.df["RETAIL SALES"].sum())
        cls.py_warehouse_total = float(cls.df["WAREHOUSE SALES"].sum())
        cls.py_transfers_total = float(cls.df["RETAIL TRANSFERS"].sum())

        # 2. Independent SQL computation
        cls.conn = sqlite3.connect(DB_PATH)
        cursor = cls.conn.cursor()

        cursor.execute("SELECT ROUND(SUM(retail_sales), 2) FROM sales;")
        cls.sql_retail_total = float(cursor.fetchone()[0])

        cursor.execute("SELECT ROUND(SUM(warehouse_sales), 2) FROM sales;")
        cls.sql_warehouse_total = float(cursor.fetchone()[0])

        cursor.execute("SELECT ROUND(SUM(retail_transfers), 2) FROM sales;")
        cls.sql_transfers_total = float(cursor.fetchone()[0])

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_01_total_retail_sales_reconciliation(self):
        diff = abs(self.py_retail_total - self.sql_retail_total)
        print(f"\n  [Cross-Engine] Retail Sales     : Python={self.py_retail_total:,.2f} | SQL={self.sql_retail_total:,.2f} | Diff={diff:.4f}")
        self.assertAlmostEqual(
            self.py_retail_total,
            self.sql_retail_total,
            delta=0.05,
            msg=f"Total retail sales mismatch: Python={self.py_retail_total} vs SQL={self.sql_retail_total}"
        )

    def test_02_total_warehouse_sales_reconciliation(self):
        diff = abs(self.py_warehouse_total - self.sql_warehouse_total)
        print(f"  [Cross-Engine] Warehouse Sales  : Python={self.py_warehouse_total:,.2f} | SQL={self.sql_warehouse_total:,.2f} | Diff={diff:.4f}")
        self.assertAlmostEqual(
            self.py_warehouse_total,
            self.sql_warehouse_total,
            delta=0.05,
            msg=f"Total warehouse sales mismatch: Python={self.py_warehouse_total} vs SQL={self.sql_warehouse_total}"
        )

    def test_03_total_retail_transfers_reconciliation(self):
        diff = abs(self.py_transfers_total - self.sql_transfers_total)
        print(f"  [Cross-Engine] Retail Transfers : Python={self.py_transfers_total:,.2f} | SQL={self.sql_transfers_total:,.2f} | Diff={diff:.4f}")
        self.assertAlmostEqual(
            self.py_transfers_total,
            self.sql_transfers_total,
            delta=0.05,
            msg=f"Total retail transfers mismatch: Python={self.py_transfers_total} vs SQL={self.sql_transfers_total}"
        )

    def test_04_item_type_reconciliation(self):
        py_by_type = self.df.groupby("ITEM TYPE")["RETAIL SALES"].sum().to_dict()
        cursor = self.conn.cursor()
        cursor.execute("SELECT item_type, ROUND(SUM(retail_sales), 2) FROM sales GROUP BY item_type;")
        sql_by_type = {row[0]: row[1] for row in cursor.fetchall()}

        for itype, py_val in py_by_type.items():
            self.assertIn(itype, sql_by_type, f"Item type {itype} missing in SQL results")
            sql_val = sql_by_type[itype]
            self.assertAlmostEqual(
                py_val,
                sql_val,
                delta=0.05,
                msg=f"Mismatch for item type '{itype}': Python={py_val} vs SQL={sql_val}"
            )

    def test_05_top_5_suppliers_reconciliation(self):
        py_top5 = self.df.groupby("SUPPLIER")["RETAIL SALES"].sum().sort_values(ascending=False).head(5)
        cursor = self.conn.cursor()
        cursor.execute("SELECT supplier, ROUND(SUM(retail_sales), 2) FROM sales GROUP BY supplier ORDER BY SUM(retail_sales) DESC LIMIT 5;")
        sql_top5 = cursor.fetchall()

        for (py_supp, py_vol), (sql_supp, sql_vol) in zip(py_top5.items(), sql_top5):
            self.assertEqual(py_supp, sql_supp)
            self.assertAlmostEqual(py_vol, sql_vol, delta=0.05)


if __name__ == "__main__":
    unittest.main()
