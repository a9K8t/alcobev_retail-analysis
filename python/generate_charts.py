"""
generate_charts.py
==================
Generates publication-quality visualizations for the Retail & Warehouse
Sales Analytics dashboard.

Charts produced (saved to Dashboard/ at 300 DPI):
1. monthly_retail_sales.png         - Monthly Retail Sales Trend (Volume)
2. sales_by_item_type.png          - Retail Sales Volume by Item Type
3. top_suppliers.png               - Top 10 Suppliers by Retail Volume
4. top_products.png                - Top 10 Products by Retail Volume
5. yearly_sales_comparison.png     - Yearly Retail vs Warehouse vs Transfers
6. retail_transfers_trend.png      - Monthly Retail Transfers Trend
7. retail_vs_warehouse_comparison.png - Channel Movement Comparison & Ratio
8. supplier_contribution.png       - Pareto Supplier Contribution & Cumulative Share
"""

import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd
import numpy as np

# Styling configuration
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Arial", "sans-serif"]
plt.rcParams["axes.edgecolor"] = "#cccccc"
plt.rcParams["axes.linewidth"] = 0.8

DASHBOARD_DIR = os.path.join(os.path.dirname(__file__), "..", "Dashboard")
CLEANED_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned_sales.csv")


def load_data():
    if not os.path.exists(CLEANED_DATA_PATH):
        raise FileNotFoundError(f"Cleaned dataset not found at {CLEANED_DATA_PATH}")
    return pd.read_csv(CLEANED_DATA_PATH)


def chart_1_monthly_retail_sales(df):
    """Chart 1: Monthly Retail Sales Trend."""
    monthly = df.groupby(["YEAR", "MONTH"])["RETAIL SALES"].sum().reset_index()
    monthly["date_str"] = monthly["YEAR"].astype(str) + "-" + monthly["MONTH"].astype(str).str.zfill(2)
    monthly["date"] = pd.to_datetime(monthly["date_str"] + "-01")
    monthly = monthly.sort_values("date").reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(13, 6), dpi=300)
    ax.plot(monthly["date_str"], monthly["RETAIL SALES"], marker="o", color="#1f77b4", linewidth=2.5, markersize=6)
    
    # Peak annotation
    peak_idx = monthly["RETAIL SALES"].idxmax()
    peak_val = monthly.loc[peak_idx, "RETAIL SALES"]
    peak_date = monthly.loc[peak_idx, "date_str"]
    ax.annotate(
        f"Holiday Peak: {peak_val:,.0f}\n({peak_date})",
        xy=(peak_idx, peak_val),
        xytext=(peak_idx - 3, peak_val + 7000),
        arrowprops=dict(facecolor="#d62728", shrink=0.08, width=1.5, headwidth=6),
        fontsize=10, fontweight="bold", color="#d62728"
    )

    ax.set_title("Monthly Retail Sales Movement Volume (2017 - 2020)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Reporting Month (YYYY-MM)", fontsize=11, labelpad=10)
    ax.set_ylabel("Retail Volume (Cases / Units)", fontsize=11, labelpad=10)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x/1000):,}K"))
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.tight_layout()

    out_path = os.path.join(DASHBOARD_DIR, "monthly_retail_sales.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print("  [OK] Generated: Dashboard/monthly_retail_sales.png")


def chart_2_sales_by_item_type(df):
    """Chart 2: Retail Sales by Item Type."""
    item_types = df.groupby("ITEM TYPE")["RETAIL SALES"].sum().sort_values(ascending=True)
    item_types = item_types[item_types > 500]  # Filter negligible categories

    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    colors = ["#aec7e8", "#98df8a", "#ffbb78", "#2ca02c", "#ff7f0e", "#1f77b4"][-len(item_types):]
    bars = ax.barh(item_types.index, item_types.values, color=colors, edgecolor="#444444", linewidth=0.6, height=0.65)

    # Bar value labels
    total = item_types.sum()
    for bar in bars:
        width = bar.get_width()
        pct = (width / total) * 100
        ax.text(width + 12000, bar.get_y() + bar.get_height()/2, f"{width:,.0f} ({pct:.1f}%)",
                va="center", ha="left", fontsize=9, fontweight="bold", color="#333333")

    ax.set_xlim(0, item_types.max() * 1.22)
    ax.set_title("Retail Sales Volume by Item Type", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Total Retail Sales Volume (Cases / Units)", fontsize=11, labelpad=10)
    ax.set_ylabel("Item Type", fontsize=11)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x/1000):,}K"))
    plt.tight_layout()

    out_path = os.path.join(DASHBOARD_DIR, "sales_by_item_type.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print("  [OK] Generated: Dashboard/sales_by_item_type.png")


def chart_3_top_suppliers(df):
    """Chart 3: Top 10 Suppliers by Retail Volume."""
    top_supp = df.groupby("SUPPLIER")["RETAIL SALES"].sum().sort_values(ascending=True).tail(10)

    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=300)
    bars = ax.barh(top_supp.index, top_supp.values, color="#2b5c8f", edgecolor="#1a365d", linewidth=0.7, height=0.65)

    total_retail = df["RETAIL SALES"].sum()
    for bar in bars:
        w = bar.get_width()
        pct = (w / total_retail) * 100
        ax.text(w + 2500, bar.get_y() + bar.get_height()/2, f"{w:,.0f} ({pct:.2f}%)",
                va="center", ha="left", fontsize=9, fontweight="semibold")

    ax.set_xlim(0, top_supp.max() * 1.25)
    ax.set_title("Top 10 Suppliers by Retail Sales Volume", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Retail Volume (Cases / Units)", fontsize=11, labelpad=10)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x/1000):,}K"))
    plt.tight_layout()

    out_path = os.path.join(DASHBOARD_DIR, "top_suppliers.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print("  [OK] Generated: Dashboard/top_suppliers.png")


def chart_4_top_products(df):
    """Chart 4: Top 10 Products by Retail Volume."""
    top_prod = df.groupby("ITEM DESCRIPTION")["RETAIL SALES"].sum().sort_values(ascending=True).tail(10)

    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=300)
    bars = ax.barh(top_prod.index, top_prod.values, color="#388e3c", edgecolor="#1b5e20", linewidth=0.7, height=0.65)

    for bar in bars:
        w = bar.get_width()
        ax.text(w + 350, bar.get_y() + bar.get_height()/2, f"{w:,.0f}",
                va="center", ha="left", fontsize=9, fontweight="semibold")

    ax.set_xlim(0, top_prod.max() * 1.18)
    ax.set_title("Top 10 Products by Retail Sales Volume", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Retail Volume (Cases / Units)", fontsize=11, labelpad=10)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x/1000):,}K"))
    plt.tight_layout()

    out_path = os.path.join(DASHBOARD_DIR, "top_products.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print("  [OK] Generated: Dashboard/top_products.png")


def chart_5_yearly_sales_comparison(df):
    """Chart 5: Yearly Retail vs Warehouse vs Transfers."""
    yearly = df.groupby("YEAR")[["RETAIL SALES", "WAREHOUSE SALES", "RETAIL TRANSFERS"]].sum()

    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    x = np.arange(len(yearly.index))
    width = 0.26

    r1 = ax.bar(x - width, yearly["RETAIL SALES"], width, label="Retail Sales", color="#1f77b4", edgecolor="#0e4b75")
    r2 = ax.bar(x, yearly["WAREHOUSE SALES"], width, label="Warehouse Sales", color="#ff7f0e", edgecolor="#b85400")
    r3 = ax.bar(x + width, yearly["RETAIL TRANSFERS"], width, label="Retail Transfers", color="#2ca02c", edgecolor="#1a6e1a")

    ax.set_title("Yearly Movement Volume by Channel (Retail / Warehouse / Transfers)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Year (Note: 2018 has 2 mos, 2020 has 4 mos)", fontsize=11, labelpad=10)
    ax.set_ylabel("Volume (Cases / Units)", fontsize=11, labelpad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(yearly.index, fontsize=10)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, p: f"{y/1e6:.1f}M"))
    ax.legend(frameon=True, facecolor="white", edgecolor="#cccccc", fontsize=10)
    plt.tight_layout()

    out_path = os.path.join(DASHBOARD_DIR, "yearly_sales_comparison.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print("  [OK] Generated: Dashboard/yearly_sales_comparison.png")


def chart_6_retail_transfers_trend(df):
    """Chart 6: Retail Transfers Monthly Trend."""
    monthly = df.groupby(["YEAR", "MONTH"])[["RETAIL SALES", "RETAIL TRANSFERS"]].sum().reset_index()
    monthly["date_str"] = monthly["YEAR"].astype(str) + "-" + monthly["MONTH"].astype(str).str.zfill(2)

    fig, ax = plt.subplots(figsize=(13, 6), dpi=300)
    ax.plot(monthly["date_str"], monthly["RETAIL TRANSFERS"], marker="s", color="#2ca02c", linewidth=2.5, label="Retail Transfers")
    ax.plot(monthly["date_str"], monthly["RETAIL SALES"], marker="o", color="#1f77b4", linewidth=1.8, linestyle="--", alpha=0.7, label="Retail Sales")

    ax.set_title("Monthly Retail Transfers vs Retail Sales Volume (Replenishment Tracking)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Reporting Month (YYYY-MM)", fontsize=11, labelpad=10)
    ax.set_ylabel("Volume (Cases / Units)", fontsize=11, labelpad=10)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x/1000):,}K"))
    plt.xticks(rotation=45, ha="right", fontsize=9)
    ax.legend(frameon=True, facecolor="white", edgecolor="#cccccc", fontsize=10)
    plt.tight_layout()

    out_path = os.path.join(DASHBOARD_DIR, "retail_transfers_trend.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print("  [OK] Generated: Dashboard/retail_transfers_trend.png")


def chart_7_retail_vs_warehouse_comparison(df):
    """Chart 7: Retail vs Warehouse Volume Comparison & Channel Share."""
    totals = [df["RETAIL SALES"].sum(), df["WAREHOUSE SALES"].sum(), df["RETAIL TRANSFERS"].sum()]
    labels = ["Retail Sales\n(2.16M / 17.9%)", "Warehouse Sales\n(7.78M / 64.4%)", "Retail Transfers\n(2.13M / 17.7%)"]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)

    # Bar chart
    bars = ax1.bar(labels, totals, color=colors, width=0.55, edgecolor="#333333", linewidth=0.8)
    for bar in bars:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 150000, f"{h/1e6:.2f}M",
                 ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax1.set_title("Total Volume by Channel", fontsize=13, fontweight="bold")
    ax1.set_ylabel("Volume (Cases / Units)", fontsize=11)
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, p: f"{y/1e6:.1f}M"))
    ax1.set_ylim(0, max(totals) * 1.15)

    # Pie / Donut
    wedges, texts, autotexts = ax2.pie(
        totals, labels=["Retail", "Warehouse", "Transfers"], autopct="%1.1f%%",
        startangle=140, colors=colors, textprops=dict(fontsize=10),
        wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2)
    )
    for at in autotexts:
        at.set_fontsize(10)
        at.set_fontweight("bold")
    ax2.set_title("Channel Share Breakdown", fontsize=13, fontweight="bold")

    plt.suptitle("Retail vs Warehouse Channel Movement Analysis", fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()

    out_path = os.path.join(DASHBOARD_DIR, "retail_vs_warehouse_comparison.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print("  [OK] Generated: Dashboard/retail_vs_warehouse_comparison.png")


def chart_8_supplier_contribution(df):
    """Chart 8: Pareto Supplier Contribution Curve."""
    supp = df.groupby("SUPPLIER")["RETAIL SALES"].sum().sort_values(ascending=False).reset_index()
    total_vol = supp["RETAIL SALES"].sum()
    supp["pct"] = (supp["RETAIL SALES"] / total_vol) * 100
    supp["cum_pct"] = supp["pct"].cumsum()
    top_20 = supp.head(20)

    fig, ax1 = plt.subplots(figsize=(13, 6.5), dpi=300)
    ax2 = ax1.twinx()

    x = np.arange(len(top_20))
    bars = ax1.bar(x, top_20["RETAIL SALES"], color="#1f77b4", alpha=0.85, width=0.6, label="Supplier Volume")
    line = ax2.plot(x, top_20["cum_pct"], color="#d62728", marker="o", linewidth=2.5, markersize=5, label="Cumulative %")

    ax2.axhline(50, color="#888888", linestyle=":", alpha=0.7)
    ax2.axhline(80, color="#d62728", linestyle="--", alpha=0.5)
    ax2.text(18, 81.5, "80% Pareto Line", color="#d62728", fontsize=9, fontweight="bold")

    ax1.set_title("Top 20 Suppliers: Volume and Cumulative Contribution (Pareto Analysis)", fontsize=14, fontweight="bold", pad=15)
    ax1.set_xlabel("Supplier (Ranked)", fontsize=11, labelpad=10)
    ax1.set_ylabel("Retail Volume (Cases / Units)", fontsize=11, color="#1f77b4")
    ax2.set_ylabel("Cumulative Contribution (%)", fontsize=11, color="#d62728")
    ax1.set_xticks(x)
    ax1.set_xticklabels(top_20["SUPPLIER"], rotation=60, ha="right", fontsize=8.5)
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, p: f"{int(y/1000):,}K"))
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, p: f"{int(y)}%"))
    ax2.set_ylim(0, 105)
    ax2.grid(False)

    plt.tight_layout()
    out_path = os.path.join(DASHBOARD_DIR, "supplier_contribution.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print("  [OK] Generated: Dashboard/supplier_contribution.png")


def generate_all_charts():
    """Generates all 8 dashboard charts."""
    print("=" * 70)
    print("GENERATING DASHBOARD VISUALIZATIONS (300 DPI)")
    print("=" * 70)
    os.makedirs(DASHBOARD_DIR, exist_ok=True)
    df = load_data()

    chart_1_monthly_retail_sales(df)
    chart_2_sales_by_item_type(df)
    chart_3_top_suppliers(df)
    chart_4_top_products(df)
    chart_5_yearly_sales_comparison(df)
    chart_6_retail_transfers_trend(df)
    chart_7_retail_vs_warehouse_comparison(df)
    chart_8_supplier_contribution(df)

    print("=" * 70)
    print(f"All 8 charts successfully written to: {DASHBOARD_DIR}")
    print("=" * 70)


if __name__ == "__main__":
    generate_all_charts()
