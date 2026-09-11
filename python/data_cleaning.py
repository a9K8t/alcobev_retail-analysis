"""
data_cleaning.py
================
Pipeline for cleaning and validating the Retail & Warehouse Sales dataset.

Raw dataset: data/Warehouse_and_Retail_Sales.csv (307,645 rows)
Cleaned output: data/cleaned_sales.csv (307,642 rows)

Cleaning decisions:
1. Rows with null 'RETAIL SALES' (3 records: indices 18390, 299150, 300935)
   are dropped because retail sales volume is a primary target metric and
   these records also lack supplier data.
2. Null 'SUPPLIER' records (164 remaining) are imputed with 'Unknown'.
3. Null 'ITEM TYPE' records (1 record: row 96129) are imputed with 'Unknown'.
4. Numeric columns ('RETAIL SALES', 'RETAIL TRANSFERS', 'WAREHOUSE SALES')
   are cast to float and rounded to 2 decimal places.
5. Text columns are stripped of leading/trailing whitespace.
6. Negative values are preserved as they represent legitimate return/reversal transactions.
"""

import os
import pandas as pd
import numpy as np

RAW_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "Warehouse_and_Retail_Sales.csv")
CLEANED_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned_sales.csv")


def clean_sales_data(input_path=RAW_DATA_PATH, output_path=CLEANED_DATA_PATH):
    """
    Loads raw sales dataset, applies cleaning transformations, validates
    integrity, and exports cleaned CSV.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    print(f"[1/5] Loading raw dataset from: {input_path}")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Raw dataset not found at: {input_path}")

    df = pd.read_csv(input_path)
    initial_rows = len(df)
    print(f"      Initial shape: {df.shape[0]:,} rows, {df.shape[1]} columns")

    # 1. Inspect nulls
    null_counts = df.isnull().sum()
    print("      Missing values detected before cleaning:")
    for col, count in null_counts[null_counts > 0].items():
        print(f"        - {col}: {count:,} missing")

    # 2. Drop rows where RETAIL SALES is NaN (3 rows)
    df = df.dropna(subset=["RETAIL SALES"]).copy()
    rows_after_dropna = len(df)
    print(f"[2/5] Dropped {initial_rows - rows_after_dropna} rows with missing 'RETAIL SALES'.")

    # 3. Impute missing categoricals
    df["SUPPLIER"] = df["SUPPLIER"].fillna("Unknown").astype(str).str.strip()
    df["ITEM TYPE"] = df["ITEM TYPE"].fillna("Unknown").astype(str).str.strip()
    df["ITEM CODE"] = df["ITEM CODE"].astype(str).str.strip()
    df["ITEM DESCRIPTION"] = df["ITEM DESCRIPTION"].astype(str).str.strip()
    print("[3/5] Imputed missing 'SUPPLIER' and 'ITEM TYPE' values with 'Unknown'.")

    # 4. Enforce proper data types
    df["YEAR"] = df["YEAR"].astype(int)
    df["MONTH"] = df["MONTH"].astype(int)

    numeric_cols = ["RETAIL SALES", "RETAIL TRANSFERS", "WAREHOUSE SALES"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0).round(2)
    print("[4/5] Cast and validated numeric columns.")

    # 5. Validation checks
    assert len(df) == 307642, f"Expected 307,642 rows, got {len(df):,}"
    assert df.isnull().sum().sum() == 0, "Cleaned dataset still contains null values!"
    assert (df["MONTH"] >= 1).all() and (df["MONTH"] <= 12).all(), "Invalid MONTH values detected!"
    assert (df["YEAR"] >= 2017).all() and (df["YEAR"] <= 2020).all(), "Invalid YEAR values detected!"

    # Save to disk
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[5/5] Exported cleaned dataset to: {output_path}")
    print(f"      Final shape: {df.shape[0]:,} rows, {df.shape[1]} columns.")

    return df


if __name__ == "__main__":
    clean_sales_data()
