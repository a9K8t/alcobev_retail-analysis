"""
test_analysis.py
================
Unit tests for Python analytics logic, KPI integrity, and chart generation.
"""

import os
import sys
import unittest
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "..", "python"))

import analysis
import generate_charts

DASHBOARD_DIR = os.path.join(BASE_DIR, "..", "Dashboard")
CLEANED_PATH = os.path.join(BASE_DIR, "..", "data", "cleaned_sales.csv")


class TestPythonAnalysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = analysis.load_cleaned_data(CLEANED_PATH)

    def test_01_kpis_calculation(self):
        kpis = analysis.compute_kpis(self.df)
        self.assertIn("total_retail_sales_volume", kpis)
        self.assertIn("total_warehouse_sales_volume", kpis)
        self.assertIn("total_retail_transfers_volume", kpis)
        self.assertIn("average_retail_sales_per_record", kpis)
        self.assertIn("retail_to_warehouse_ratio", kpis)

        self.assertGreater(kpis["total_retail_sales_volume"], 2000000)
        self.assertGreater(kpis["total_warehouse_sales_volume"], 7000000)
        self.assertGreater(kpis["total_retail_transfers_volume"], 2000000)
        self.assertEqual(kpis["total_records"], 307642)

    def test_02_item_types_analysis(self):
        item_types = analysis.analyze_item_types(self.df)
        self.assertGreaterEqual(len(item_types), 5)
        # Top item type by retail volume should be LIQUOR
        top_type = item_types.iloc[0]["ITEM TYPE"]
        self.assertEqual(top_type, "LIQUOR")
        # Shares should sum to approximately 100%
        self.assertAlmostEqual(item_types["retail_share_pct"].sum(), 100.0, places=1)

    def test_03_top_suppliers(self):
        top_supp = analysis.get_top_suppliers(self.df, top_n=10)
        self.assertEqual(len(top_supp), 10)
        # Check cumulative percentage is strictly non-decreasing and <= 100
        self.assertTrue((top_supp["cumulative_pct"].diff().dropna() >= 0).all())
        self.assertLessEqual(top_supp["cumulative_pct"].iloc[-1], 100.0)

    def test_04_top_products(self):
        top_prod = analysis.get_top_products(self.df, top_n=10)
        self.assertEqual(len(top_prod), 10)
        self.assertTrue(all(len(str(p)) > 0 for p in top_prod["item_description"]))

    def test_05_monthly_sales_periods(self):
        monthly = analysis.get_monthly_sales(self.df)
        # Must reflect the 24 distinct active calendar months
        self.assertEqual(len(monthly), 24)
        self.assertIn("date", monthly.columns)

    def test_06_yearly_sales_periods(self):
        yearly = analysis.get_yearly_sales(self.df)
        self.assertEqual(len(yearly), 4)
        self.assertListEqual(list(yearly["YEAR"]), [2017, 2018, 2019, 2020])

    def test_07_peak_and_trough_months(self):
        highest, lowest = analysis.get_peak_and_trough_months(self.df, top_n=5)
        self.assertEqual(len(highest), 5)
        self.assertEqual(len(lowest), 5)
        self.assertGreater(highest["retail_sales"].iloc[0], lowest["retail_sales"].iloc[0])

    def test_08_charts_generated_and_non_empty(self):
        expected_charts = [
            "monthly_retail_sales.png",
            "sales_by_item_type.png",
            "top_suppliers.png",
            "top_products.png",
            "yearly_sales_comparison.png",
            "retail_transfers_trend.png",
            "retail_vs_warehouse_comparison.png",
            "supplier_contribution.png"
        ]
        for chart_name in expected_charts:
            chart_path = os.path.join(DASHBOARD_DIR, chart_name)
            self.assertTrue(os.path.exists(chart_path), f"Chart not found: {chart_name}")
            # Ensure file is not an empty stub (should be > 20 KB at 300 DPI)
            self.assertGreater(os.path.getsize(chart_path), 20000, f"Chart file too small: {chart_name}")


if __name__ == "__main__":
    unittest.main()
