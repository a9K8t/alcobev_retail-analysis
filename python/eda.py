"""
eda.py
======
Exploratory Data Analysis module for the Retail & Warehouse Sales dataset.

Performs statistical profiling, distribution analysis, negative transaction
analysis (returns/reversals), channel correlations, and supplier/product concentration.
"""

import os
import pandas as pd
import numpy as np

CLEANED_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned_sales.csv")


def run_eda(data_path=CLEANED_DATA_PATH):
    """Executes full exploratory data analysis and prints structured findings."""
    print("=" * 70)
    print("EXPLORATORY DATA ANALYSIS (EDA)")
    print("Dataset: Retail & Warehouse Sales Analytics")
    print("=" * 70)

    df = pd.read_csv(data_path)
    print(f"\n1. DATASET DIMENSIONS")
    print(f"   Total Records: {len(df):,}")
    print(f"   Total Attributes: {len(df.columns)}")
    print(f"   Memory Usage: {df.memory_usage(deep=True).sum() / (1024**2):.2f} MB")

    # 2. Summary Statistics for Numeric Movement Columns
    num_cols = ["RETAIL SALES", "RETAIL TRANSFERS", "WAREHOUSE SALES"]
    print(f"\n2. NUMERICAL DISTRIBUTION STATISTICS (Volume/Cases)")
    stats = df[num_cols].describe(percentiles=[0.01, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99]).T
    stats["skew"] = df[num_cols].skew()
    stats["kurtosis"] = df[num_cols].kurtosis()
    print(stats.to_string())

    # 3. Negative Movement / Returns Analysis
    print(f"\n3. RETURNS & REVERSALS (Negative Values)")
    for col in num_cols:
        neg_mask = df[col] < 0
        neg_count = neg_mask.sum()
        neg_vol = df.loc[neg_mask, col].sum()
        print(f"   - {col:18}: {neg_count:,} records ({neg_count/len(df)*100:.3f}%), Volume: {neg_vol:,.2f}")

    # 4. Zero Volume Transactions
    print(f"\n4. ZERO VOLUME RECORDS (Inactive Products in Period)")
    for col in num_cols:
        zero_count = (df[col] == 0).sum()
        print(f"   - {col:18}: {zero_count:,} records ({zero_count/len(df)*100:.2f}%)")

    # 5. Channel Correlation Matrix
    print(f"\n5. CROSS-CHANNEL CORRELATIONS (Pearson)")
    corr = df[num_cols].corr()
    print(corr.round(4).to_string())

    # 6. Categorical Concentration (Item Types)
    print(f"\n6. ITEM TYPE SUMMARY (Volume & Share)")
    type_summary = df.groupby("ITEM TYPE").agg(
        record_count=("ITEM TYPE", "count"),
        total_retail=("RETAIL SALES", "sum"),
        total_transfers=("RETAIL TRANSFERS", "sum"),
        total_warehouse=("WAREHOUSE SALES", "sum")
    ).sort_values("total_retail", ascending=False)
    type_summary["retail_share_pct"] = (type_summary["total_retail"] / type_summary["total_retail"].sum()) * 100
    type_summary["warehouse_share_pct"] = (type_summary["total_warehouse"] / type_summary["total_warehouse"].sum()) * 100
    print(type_summary.round(2).to_string())

    # 7. Supplier Concentration (Pareto Principle)
    total_retail_vol = df["RETAIL SALES"].sum()
    supplier_vols = df.groupby("SUPPLIER")["RETAIL SALES"].sum().sort_values(ascending=False)
    top_10_vol = supplier_vols.head(10).sum()
    top_20_vol = supplier_vols.head(20).sum()
    print(f"\n7. SUPPLIER CONCENTRATION (Retail Volume)")
    print(f"   Total Distinct Suppliers: {len(supplier_vols):,}")
    print(f"   Top 10 Suppliers Volume: {top_10_vol:,.2f} ({top_10_vol / total_retail_vol * 100:.2f}%)")
    print(f"   Top 20 Suppliers Volume: {top_20_vol:,.2f} ({top_20_vol / total_retail_vol * 100:.2f}%)")

    # 8. Product Catalog Depth
    product_vols = df.groupby("ITEM DESCRIPTION")["RETAIL SALES"].sum().sort_values(ascending=False)
    top_10_prod = product_vols.head(10).sum()
    print(f"\n8. PRODUCT CATALOG DEPTH")
    print(f"   Total Distinct Products: {len(product_vols):,}")
    print(f"   Top 10 Products Volume: {top_10_prod:,.2f} ({top_10_prod / total_retail_vol * 100:.2f}%)")

    # 9. Temporal Gaps & Coverage
    print(f"\n9. TEMPORAL DISTRIBUTION (Records per Year-Month)")
    temporal = df.groupby(["YEAR", "MONTH"]).agg(
        records=("ITEM CODE", "count"),
        retail_vol=("RETAIL SALES", "sum"),
        warehouse_vol=("WAREHOUSE SALES", "sum"),
        transfers_vol=("RETAIL TRANSFERS", "sum")
    ).reset_index()
    print(f"   Total Distinct Reporting Months: {len(temporal)}")
    for _, row in temporal.iterrows():
        print(f"   {int(row['YEAR'])} - Month {int(row['MONTH']):02d}: {int(row['records']):,} records | Retail: {row['retail_vol']:>10,.1f} | Warehouse: {row['warehouse_vol']:>11,.1f}")

    print("\n" + "=" * 70)
    print("EDA COMPLETED")
    print("=" * 70)
    return {
        "dimensions": df.shape,
        "stats": stats,
        "item_types": type_summary,
        "temporal": temporal
    }


if __name__ == "__main__":
    run_eda()
