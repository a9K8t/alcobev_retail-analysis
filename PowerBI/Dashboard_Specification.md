# Power BI Dashboard Specification: Retail & Warehouse Sales Analytics

## Overview

This specification details the layout, grid architecture, visual components, interaction model, and formatting for the two-page interactive Power BI dashboard for **Retail & Warehouse Sales Analytics**.

> [!IMPORTANT]
> All metrics represent **physical volume** (cases / units). Monetary terms such as "Revenue", "Price", "Margin", or "Profit" are strictly prohibited as the underlying dataset does not support monetary figures.

---

## Canvas Architecture

- **Canvas Size**: 16:9 widescreen (1920 x 1080 px)
- **Theme Palette**:
  - Primary / Retail: `#1F77B4` (Deep Blue)
  - Secondary / Warehouse: `#FF7F0E` (Warm Amber)
  - Tertiary / Transfers: `#2CA02C` (Forest Green)
  - Dark Neutral (Text): `#212529`
  - Light Neutral (Cards/Panels): `#FFFFFF`
  - Canvas Background: `#F8F9FA`
- **Typography**: Segoe UI (Title: 18pt bold, KPI Callout: 28pt bold, Card Labels: 10pt regular, Axis: 9pt regular)

---

## Page 1: Executive Overview

### Objective
Provide executive leadership and supply chain managers with a high-level view of retail sales movement, warehouse distribution volume, inter-facility retail transfers, and category composition.

### Layout Grid (1920 x 1080)

```
+---------------------------------------------------------------------------------------------------+
|  HEADER: Retail & Warehouse Sales Analytics | Executive Overview           [Slicers: Year, Month] |
+---------------------------------------------------------------------------------------------------+
|  [KPI CARD 1]          |  [KPI CARD 2]          |  [KPI CARD 3]          |  [KPI CARD 4]          |
|  Total Retail Sales    |  Total Warehouse Sales |  Total Retail Transfers|  Avg Retail Sales/Rec  |
|  2.16M Cases           |  7.78M Cases           |  2.13M Cases           |  7.02 Units            |
+---------------------------------------------------------------------------------------------------+
|  [VISUAL 1: Left 55% Width]                     |  [VISUAL 2: Right 45% Width]                    |
|  Monthly Retail Sales Trend                     |  Retail vs Warehouse Sales by Year              |
|  (Line chart with peak holiday annotation)      |  (Grouped column chart comparing 3 streams)     |
+---------------------------------------------------------------------------------------------------+
|  [VISUAL 3: Left 50% Width]                     |  [VISUAL 4: Right 50% Width]                    |
|  Sales Volume by Item Type                      |  Top 10 Suppliers by Retail Volume              |
|  (Horizontal bar chart: Liquor, Wine, Beer...)  |  (Horizontal bar chart with % contribution)     |
+---------------------------------------------------------------------------------------------------+
```

### Visual Specifications

1. **Top Slicer Bar (Y: 0, H: 80)**:
   - Slicer 1: `YEAR` (Dropdown / Tile, multi-select, options: 2017, 2018, 2019, 2020).
   - Slicer 2: `MONTH` (Dropdown / Slider, options: 1 to 12).
2. **KPI Card Strip (Y: 90, H: 130)**:
   - Card 1: `[Total Retail Sales Volume]` formatted as `#,##0.0,, "M Cases"`.
   - Card 2: `[Total Warehouse Sales Volume]` formatted as `#,##0.0,, "M Cases"`.
   - Card 3: `[Total Retail Transfers Volume]` formatted as `#,##0.0,, "M Cases"`.
   - Card 4: `[Average Retail Sales per Record]` formatted as `#,##0.00 "Units"`.
3. **Visual 1 (Y: 230, W: 1020, H: 400)**:
   - **Type**: Line Chart.
   - **X-Axis**: `'Calendar'[Year-Month]` (Chronological).
   - **Y-Axis**: `[Total Retail Sales Volume]`.
   - **Data Labels**: On for maximum point (December 2017 peak).
4. **Visual 2 (Y: 230, W: 860, H: 400)**:
   - **Type**: Clustered Column Chart.
   - **X-Axis**: `'sales'[YEAR]`.
   - **Y-Axis**: `[Total Retail Sales Volume]`, `[Total Warehouse Sales Volume]`, `[Total Retail Transfers Volume]`.
5. **Visual 3 (Y: 640, W: 940, H: 410)**:
   - **Type**: Clustered Bar Chart (Horizontal).
   - **Y-Axis**: `'sales'[ITEM TYPE]`.
   - **X-Axis**: `[Total Retail Sales Volume]`.
   - **Data Labels**: Values + % of Total.
6. **Visual 4 (Y: 640, W: 940, H: 410)**:
   - **Type**: Clustered Bar Chart (Horizontal).
   - **Y-Axis**: `'sales'[SUPPLIER]` (Top 10 filter).
   - **X-Axis**: `[Total Retail Sales Volume]`.

---

## Page 2: Product & Supplier Analysis

### Objective
Enable category managers and inventory planners to drill down into supplier performance, brand concentration, catalog breadth, and individual SKU movement.

### Layout Grid (1920 x 1080)

```
+---------------------------------------------------------------------------------------------------+
|  HEADER: Product & Supplier Deep Dive                          [Slicers: Year, Item Type, Supplier]
+---------------------------------------------------------------------------------------------------+
|  [VISUAL 1: Top Left 50%]                       |  [VISUAL 2: Top Right 50%]                      |
|  Top 10 Products (SKUs) by Retail Volume        |  Top 10 Suppliers Pareto Contribution           |
|  (Bar chart: Tito's, Corona, Heineken, Bud...)  |  (Combo: Bar [Volume] + Line [Cumulative %])    |
+---------------------------------------------------------------------------------------------------+
|  [VISUAL 3: Bottom Left 50%]                    |  [VISUAL 4: Bottom Right 50%]                   |
|  Supplier Diversification (Breadth of Catalog)  |  Product Volume Distribution by Category        |
|  (Scatter: Distinct Item Types vs Retail Vol)   |  (Matrix Table with conditional formatting)     |
+---------------------------------------------------------------------------------------------------+
```

### Visual Specifications

1. **Top Slicers Bar**:
   - `YEAR`, `ITEM TYPE` (Multi-select pill), `SUPPLIER` (Searchable dropdown).
2. **Visual 1 (Top Left)**:
   - **Type**: Clustered Bar Chart.
   - **Y-Axis**: `'sales'[ITEM DESCRIPTION]` (Top 10 by `[Total Retail Sales Volume]`).
   - **X-Axis**: `[Total Retail Sales Volume]`.
3. **Visual 2 (Top Right)**:
   - **Type**: Line and Clustered Column Chart (Pareto).
   - **X-Axis**: `'sales'[SUPPLIER]` (Top 20).
   - **Column Y-Axis**: `[Total Retail Sales Volume]`.
   - **Line Y-Axis**: `[Cumulative Supplier Retail %]`.
4. **Visual 3 (Bottom Left)**:
   - **Type**: Scatter Chart.
   - **X-Axis**: `[Distinct Item Types Count]`.
   - **Y-Axis**: `[Total Retail Sales Volume]`.
   - **Details**: `'sales'[SUPPLIER]`.
   - **Size**: `[Total Warehouse Sales Volume]`.
5. **Visual 4 (Bottom Right)**:
   - **Type**: Matrix.
   - **Rows**: `'sales'[ITEM TYPE]`, `'sales'[ITEM DESCRIPTION]`.
   - **Values**: `[Total Retail Sales Volume]`, `[Total Warehouse Sales Volume]`, `[Retail-to-Warehouse Ratio]`.
