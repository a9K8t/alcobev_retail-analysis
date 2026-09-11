"""
test_sql.py
===========
Unit tests for SQLite database schema, table integrity, indexes,
and execution of all 18 analytical queries.
"""

import os
import sqlite3
import unittest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "SQL", "database.db")
QUERIES_DIR = os.path.join(BASE_DIR, "..", "SQL", "queries")


class TestSqlLayer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.exists(DB_PATH):
            import sys
            sys.path.insert(0, os.path.join(BASE_DIR, "..", "SQL"))
            import load_data
            load_data.init_database(db_path=DB_PATH)
        cls.conn = sqlite3.connect(DB_PATH)

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_01_database_exists(self):
        self.assertTrue(os.path.exists(DB_PATH), f"Database not found at {DB_PATH}")

    def test_02_sales_table_row_count(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sales;")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 307642, f"Expected 307,642 records, found {count}")

    def test_03_indexes_exist(self):
        cursor = self.conn.cursor()
        cursor.execute("PRAGMA index_list('sales');")
        indexes = cursor.fetchall()
        # Expect at least 4 custom indexes
        self.assertGreaterEqual(len(indexes), 4)

    def test_04_all_18_queries_execute_cleanly(self):
        cursor = self.conn.cursor()
        query_files = sorted([f for f in os.listdir(QUERIES_DIR) if f.endswith(".sql")])
        self.assertEqual(len(query_files), 18, f"Expected 18 queries, found {len(query_files)}")

        for fname in query_files:
            with self.subTest(query_file=fname):
                fpath = os.path.join(QUERIES_DIR, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    sql = f.read()
                cursor.execute(sql)
                rows = cursor.fetchall()
                self.assertIsNotNone(rows, f"Query {fname} returned None")
                self.assertGreater(len(rows), 0, f"Query {fname} returned zero rows")


if __name__ == "__main__":
    unittest.main()
