# Power BI Visuals Guide: Retail & Warehouse Sales Analytics

Detailed field mappings, visual properties, filter configurations, and interactive behaviors for all visuals.

---

## Page 1: Executive Overview

### 1. KPI Callout Cards (Header Strip)

| Card Name | Measure / Field | Display Units | Title / Subtitle |
|---|---|---|---|
| **Card 1** | `[Total Retail Sales Volume]` | Millions (`M`) | Title: "Retail Sales Volume", Subtitle: "Total store movement" |
| **Card 2** | `[Total Warehouse Sales Volume]` | Millions (`M`) | Title: "Warehouse Sales Volume", Subtitle: "Total wholesale movement" |
| **Card 3** | `[Total Retail Transfers Volume]` | Millions (`M`) | Title: "Retail Transfers Volume", Subtitle: "Store replenishment movement" |
| **Card 4** | `[Average Retail Sales per Record]` | None | Title: "Average Retail Volume", Subtitle: "Per line-item transaction" |

---

### 2. Monthly Retail Sales Trend

- **Visual Type**: Line Chart
- **X-Axis**: `'Calendar'[Year-Month]` (Categorical or Continuous)
- **Y-Axis**: `[Total Retail Sales Volume]`
- **Secondary Y-Axis**: *(Optional)* `[Total Retail Transfers Volume]`
- **Tooltips**:
  - `'Calendar'[Year]`
  - `'Calendar'[Month Name]`
  - `[Total Retail Sales Volume]`
  - `[YoY Retail Sales Growth %]`
- **Visual-Level Filter**: None
- **Formatting**:
  - Line stroke width: 3px, color `#1F77B4`
  - Data markers: On (circle, 5px)
  - Reference Line: Maximum line showing peak month (Dec 2017)

---

### 3. Retail vs Warehouse Sales by Year

- **Visual Type**: Clustered Column Chart
- **X-Axis**: `'Calendar'[Year]`
- **Y-Axis**:
  - `[Total Retail Sales Volume]` (Color: `#1F77B4`)
  - `[Total Warehouse Sales Volume]` (Color: `#FF7F0E`)
  - `[Total Retail Transfers Volume]` (Color: `#2CA02C`)
- **Data Labels**: On (Position: Outside End, Display Units: `Millions`)
- **Y-Axis Range**: Auto

---

### 4. Retail Sales Volume by Item Type

- **Visual Type**: Clustered Bar Chart (Horizontal)
- **Y-Axis**: `'sales'[ITEM TYPE]`
- **X-Axis**: `[Total Retail Sales Volume]`
- **Tooltips**:
  - `[Retail Sales % of Total]`
  - `[Total Warehouse Sales Volume]`
  - `[Distinct Products Count]`
- **Sort**: By `[Total Retail Sales Volume]` Descending
- **Visual Filter**: `[Total Retail Sales Volume] > 1000` (removes noise/adjustments)

---

### 5. Top 10 Suppliers by Retail Volume

- **Visual Type**: Clustered Bar Chart (Horizontal)
- **Y-Axis**: `'sales'[SUPPLIER]`
- **X-Axis**: `[Total Retail Sales Volume]`
- **Visual-Level Filter**: Top N by `[Total Retail Sales Volume]`, Top `10`
- **Data Labels**: On (Values + `% of Total`)
- **Color**: Solid Deep Blue (`#2B5C8F`)

---

## Page 2: Product & Supplier Analysis

### 1. Top 10 Products (SKUs) by Retail Volume

- **Visual Type**: Clustered Bar Chart (Horizontal)
- **Y-Axis**: `'sales'[ITEM DESCRIPTION]`
- **X-Axis**: `[Total Retail Sales Volume]`
- **Visual-Level Filter**: Top N on `'sales'[ITEM DESCRIPTION]` by `[Total Retail Sales Volume]`, Top `10`
- **Data Labels**: On (Formatted with commas)
- **Color**: Emerald Green (`#388E3C`)

---

### 2. Supplier Pareto Contribution

- **Visual Type**: Line and Clustered Column Chart
- **Shared X-Axis**: `'sales'[SUPPLIER]`
- **Column Y-Axis**: `[Total Retail Sales Volume]` (Bar color: `#1F77B4`)
- **Line Y-Axis**: `[Cumulative Supplier Retail %]` (Line color: `#D62728`)
- **Visual-Level Filter**: Top N on `'sales'[SUPPLIER]` by `[Total Retail Sales Volume]`, Top `20`
- **Constant Line**: Secondary Y-Axis constant line at `80%` (Dashed red line for 80/20 rule)

---

### 3. Supplier Diversification (Catalog Breadth)

- **Visual Type**: Scatter Chart
- **Details**: `'sales'[SUPPLIER]`
- **X-Axis**: `[Distinct Item Types Count]`
- **Y-Axis**: `[Total Retail Sales Volume]`
- **Size**: `[Total Warehouse Sales Volume]`
- **Color**: By primary `'sales'[ITEM TYPE]` dominant category
- **Visual-Level Filter**: `[Total Retail Sales Volume] > 5000`

---

### 4. Product Catalog Movement Matrix

- **Visual Type**: Matrix Table
- **Rows**:
  - Level 1: `'sales'[ITEM TYPE]`
  - Level 2: `'sales'[ITEM DESCRIPTION]`
- **Values**:
  - `[Total Retail Sales Volume]`
  - `[Total Warehouse Sales Volume]`
  - `[Total Retail Transfers Volume]`
  - `[Retail-to-Warehouse Ratio]`
- **Conditional Formatting**: Data bars on `[Total Retail Sales Volume]`
