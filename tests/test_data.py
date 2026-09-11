"""
test_data.py
============
Unit tests for data validation, cleaning integrity, and schema adherence.
"""

import os
import unittest
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_PATH = os.path.join(BASE_DIR, "..", "data", "Warehouse_and_Retail_Sales.csv")
CLEANED_PATH = os.path.join(BASE_DIR, "..", "data", "cleaned_sales.csv")


class TestDataIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.exists(CLEANED_PATH):
            import sys
            sys.path.insert(0, os.path.join(BASE_DIR, "..", "python"))
            from data_cleaning import clean_sales_data
            clean_sales_data(input_path=RAW_PATH, output_path=CLEANED_PATH)
        cls.df = pd.read_csv(CLEANED_PATH)

    def test_01_raw_data_exists(self):
        self.assertTrue(os.path.exists(RAW_PATH), f"Raw dataset not found at {RAW_PATH}")

    def test_02_cleaned_data_exists(self):
        self.assertTrue(os.path.exists(CLEANED_PATH), f"Cleaned dataset not found at {CLEANED_PATH}")

    def test_03_cleaned_data_row_count(self):
        self.assertEqual(len(self.df), 307642, f"Expected 307,642 rows, found {len(self.df)}")

    def test_04_required_columns_exist(self):
        expected_cols = [
            "YEAR", "MONTH", "SUPPLIER", "ITEM CODE",
            "ITEM DESCRIPTION", "ITEM TYPE", "RETAIL SALES",
            "RETAIL TRANSFERS", "WAREHOUSE SALES"
        ]
        self.assertListEqual(list(self.df.columns), expected_cols)

    def test_05_no_null_values_in_cleaned_data(self):
        null_total = self.df.isnull().sum().sum()
        self.assertEqual(null_total, 0, f"Found {null_total} null values in cleaned dataset")

    def test_06_numeric_column_types(self):
        for col in ["RETAIL SALES", "RETAIL TRANSFERS", "WAREHOUSE SALES"]:
            self.assertTrue(
                pd.api.types.is_numeric_dtype(self.df[col]),
                f"Column {col} is not numeric: {self.df[col].dtype}"
            )

    def test_07_year_values_valid(self):
        valid_years = {2017, 2018, 2019, 2020}
        actual_years = set(self.df["YEAR"].unique())
        self.assertTrue(actual_years.issubset(valid_years), f"Unexpected years found: {actual_years - valid_years}")

    def test_08_month_values_valid(self):
        min_month = self.df["MONTH"].min()
        max_month = self.df["MONTH"].max()
        self.assertGreaterEqual(min_month, 1)
        self.assertLessEqual(max_month, 12)


if __name__ == "__main__":
    unittest.main()
