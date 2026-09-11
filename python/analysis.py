"""
analysis.py
===========
Business analytics and KPI calculation engine for Retail & Warehouse Sales.

Consumes cleaned data from data/cleaned_sales.csv and produces core KPIs,
item-type distributions, supplier/product rankings, Pareto contributions,
temporal metrics, and YoY growth calculations.

All metrics represent physical movement/sales volume (cases/units).
No financial revenue, prices, margins, or profits are assumed or fabricated.
"""

import os
import pandas as pd
import numpy as np

CLEANED_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned_sales.csv")


def load_cleaned_data(path=CLEANED_DATA_PATH):
    """Loads and validates cleaned dataset from CSV."""
    if not os.path.exists(path):
        from data_cleaning import clean_sales_data
        return clean_sales_data(output_path=path)
    return pd.read_csv(path)


def compute_kpis(df):
    """Computes headline volume KPIs."""
    total_retail = float(df["RETAIL SALES"].sum())
    total_warehouse = float(df["WAREHOUSE SALES"].sum())
    total_transfers = float(df["RETAIL TRANSFERS"].sum())
    avg_retail = float(df["RETAIL SALES"].mean())
    ratio_retail_wh = total_retail / total_warehouse if total_warehouse != 0 else 0.0

    return {
        "total_retail_sales_volume": round(total_retail, 2),
        "total_warehouse_sales_volume": round(total_warehouse, 2),
        "total_retail_transfers_volume": round(total_transfers, 2),
        "average_retail_sales_per_record": round(avg_retail, 4),
        "retail_to_warehouse_ratio": round(ratio_retail_wh, 4),
        "total_records": len(df)
    }


def analyze_item_types(df):
    """Aggregates retail, warehouse, and transfer volumes by item type."""
    agg = df.groupby("ITEM TYPE").agg(
        total_retail_sales=("RETAIL SALES", "sum"),
        total_warehouse_sales=("WAREHOUSE SALES", "sum"),
        total_retail_transfers=("RETAIL TRANSFERS", "sum"),
        record_count=("ITEM TYPE", "count")
    ).reset_index()
    agg["retail_share_pct"] = (agg["total_retail_sales"] / agg["total_retail_sales"].sum()) * 100
    for col in ["total_retail_sales", "total_warehouse_sales", "total_retail_transfers", "retail_share_pct"]:
        agg[col] = agg[col].round(2)
    return agg.sort_values("total_retail_sales", ascending=False)


def get_top_suppliers(df, top_n=10):
    """Calculates top suppliers by retail sales volume with market share and cumulative %."""
    total_retail = df["RETAIL SALES"].sum()
    supp = df.groupby("SUPPLIER")["RETAIL SALES"].sum().reset_index()
    supp.columns = ["supplier", "retail_sales"]
    supp = supp.sort_values("retail_sales", ascending=False).reset_index(drop=True)
    supp["pct_of_total"] = (supp["retail_sales"] / total_retail) * 100
    supp["cumulative_pct"] = supp["pct_of_total"].cumsum()
    supp["retail_sales"] = supp["retail_sales"].round(2)
    supp["pct_of_total"] = supp["pct_of_total"].round(3)
    supp["cumulative_pct"] = supp["cumulative_pct"].round(3)
    return supp.head(top_n)


def get_top_products(df, top_n=10):
    """Calculates top products by retail sales volume with percentage of total."""
    total_retail = df["RETAIL SALES"].sum()
    prod = df.groupby("ITEM DESCRIPTION")["RETAIL SALES"].sum().reset_index()
    prod.columns = ["item_description", "retail_sales"]
    prod = prod.sort_values("retail_sales", ascending=False).reset_index(drop=True)
    prod["pct_of_total"] = (prod["retail_sales"] / total_retail) * 100
    prod["retail_sales"] = prod["retail_sales"].round(2)
    prod["pct_of_total"] = prod["pct_of_total"].round(3)
    return prod.head(top_n)


def get_monthly_sales(df):
    """Aggregates monthly sales and creates chronological datetime column."""
    monthly = df.groupby(["YEAR", "MONTH"]).agg(
        retail_sales=("RETAIL SALES", "sum"),
        warehouse_sales=("WAREHOUSE SALES", "sum"),
        retail_transfers=("RETAIL TRANSFERS", "sum"),
        record_count=("ITEM CODE", "count")
    ).reset_index()
    for col in ["retail_sales", "warehouse_sales", "retail_transfers"]:
        monthly[col] = monthly[col].round(2)
    monthly["date"] = pd.to_datetime(
        monthly["YEAR"].astype(str) + "-" + monthly["MONTH"].astype(str).str.zfill(2) + "-01"
    )
    return monthly.sort_values("date").reset_index(drop=True)


def get_yearly_sales(df):
    """Aggregates yearly sales and computes retail-to-warehouse ratio."""
    yearly = df.groupby("YEAR").agg(
        retail_sales=("RETAIL SALES", "sum"),
        warehouse_sales=("WAREHOUSE SALES", "sum"),
        retail_transfers=("RETAIL TRANSFERS", "sum")
    ).reset_index()
    yearly["retail_to_warehouse_ratio"] = (yearly["retail_sales"] / yearly["warehouse_sales"]).round(4)
    for col in ["retail_sales", "warehouse_sales", "retail_transfers"]:
        yearly[col] = yearly[col].round(2)
    return yearly


def get_yoy_growth(df):
    """Calculates Year-over-Year retail volume growth rate using prior-year comparison."""
    yearly = df.groupby("YEAR")["RETAIL SALES"].sum().reset_index()
    yearly.columns = ["year", "retail_sales"]
    yearly = yearly.sort_values("year").reset_index(drop=True)
    yearly["prior_year_sales"] = yearly["retail_sales"].shift(1)
    yearly["yoy_growth_pct"] = (
        (yearly["retail_sales"] - yearly["prior_year_sales"]) / yearly["prior_year_sales"] * 100
    ).round(2)
    yearly["retail_sales"] = yearly["retail_sales"].round(2)
    yearly["prior_year_sales"] = yearly["prior_year_sales"].round(2)
    return yearly


def get_peak_and_trough_months(df, top_n=5):
    """Finds highest and lowest performing calendar months by retail volume."""
    monthly = get_monthly_sales(df)
    highest = monthly.sort_values("retail_sales", ascending=False).head(top_n)[["YEAR", "MONTH", "retail_sales"]]
    lowest = monthly.sort_values("retail_sales", ascending=True).head(top_n)[["YEAR", "MONTH", "retail_sales"]]
    return highest.reset_index(drop=True), lowest.reset_index(drop=True)


def run_full_analysis():
    """Runs end-to-end analytical pipeline and outputs formatted results."""
    print("=" * 75)
    print("RETAIL & WAREHOUSE SALES ANALYTICS - PYTHON ANALYSIS SUITE")
    print("=" * 75)

    df = load_cleaned_data()
    kpis = compute_kpis(df)

    print("\n[1] HEADLINE BUSINESS KPIs (Volume/Units)")
    print(f"    - Total Retail Sales Volume     : {kpis['total_retail_sales_volume']:>14,f}")
    print(f"    - Total Warehouse Sales Volume  : {kpis['total_warehouse_sales_volume']:>14,f}")
    print(f"    - Total Retail Transfers Volume : {kpis['total_retail_transfers_volume']:>14,f}")
    print(f"    - Average Retail Sales/Record   : {kpis['average_retail_sales_per_record']:>14.4f}")
    print(f"    - Retail-to-Warehouse Ratio     : {kpis['retail_to_warehouse_ratio']:>14.4f}")
    print(f"    - Total Cleaned Records         : {kpis['total_records']:>14,d}")

    print("\n[2] TOP 5 ITEM TYPES BY RETAIL VOLUME")
    item_types = analyze_item_types(df)
    print(item_types.head(5).to_string(index=False))

    print("\n[3] TOP 10 SUPPLIERS (Pareto Contribution)")
    top_supp = get_top_suppliers(df, top_n=10)
    print(top_supp.to_string(index=False))

    print("\n[4] TOP 10 PRODUCTS BY RETAIL VOLUME")
    top_prod = get_top_products(df, top_n=10)
    print(top_prod.to_string(index=False))

    print("\n[5] YEARLY VOLUME BREAKDOWN")
    yearly = get_yearly_sales(df)
    print(yearly.to_string(index=False))

    print("\n[6] YEAR-OVER-YEAR RETAIL GROWTH")
    yoy = get_yoy_growth(df)
    print(yoy.to_string(index=False))

    highest_months, lowest_months = get_peak_and_trough_months(df, top_n=5)
    print("\n[7] TOP 5 HIGHEST-PERFORMING MONTHS")
    print(highest_months.to_string(index=False))

    print("\n[8] TOP 5 LOWEST-PERFORMING MONTHS")
    print(lowest_months.to_string(index=False))

    print("\n" + "=" * 75)
    print("ANALYSIS COMPLETE")
    print("=" * 75)

    return {
        "kpis": kpis,
        "item_types": item_types,
        "top_suppliers": top_supp,
        "top_products": top_prod,
        "yearly": yearly,
        "yoy": yoy,
        "highest_months": highest_months,
        "lowest_months": lowest_months
    }


if __name__ == "__main__":
    run_full_analysis()
