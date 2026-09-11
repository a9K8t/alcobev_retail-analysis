# DAX Measures Catalog: Retail & Warehouse Sales Analytics

This document details all DAX measures required for the Power BI dashboard, organized into a dedicated `_Measures` table.

> [!NOTE]
> All formulas use actual column names from `data/cleaned_sales.csv` and adhere strictly to volume semantics.

---

## 1. Core Volume Measures (Cases / Units)

### Total Retail Sales Volume
```dax
Total Retail Sales Volume = 
SUM ( 'sales'[RETAIL SALES] )
```
- **Format**: `#,##0.00` (or `#,##0.0,, "M"` in card display units)
- **Description**: Sum of all store retail movement units.

### Total Warehouse Sales Volume
```dax
Total Warehouse Sales Volume = 
SUM ( 'sales'[WAREHOUSE SALES] )
```
- **Format**: `#,##0.00`
- **Description**: Sum of wholesale movement from central warehouse to licensees.

### Total Retail Transfers Volume
```dax
Total Retail Transfers Volume = 
SUM ( 'sales'[RETAIL TRANSFERS] )
```
- **Format**: `#,##0.00`
- **Description**: Sum of stock movement transferred from warehouse to retail stores.

### Total Movement Volume
```dax
Total Movement Volume = 
[Total Retail Sales Volume] + [Total Warehouse Sales Volume] + [Total Retail Transfers Volume]
```
- **Format**: `#,##0.00`
- **Description**: Combined supply chain logistics movement.

---

## 2. Ratios & Channel Share

### Retail-to-Warehouse Ratio
```dax
Retail-to-Warehouse Ratio = 
DIVIDE ( 
    [Total Retail Sales Volume], 
    [Total Warehouse Sales Volume], 
    BLANK () 
)
```
- **Format**: `0.0000`
- **Description**: Measures the ratio of direct-to-consumer store sales versus wholesale distribution.

### Retail Channel Share %
```dax
Retail Channel Share % = 
DIVIDE ( 
    [Total Retail Sales Volume], 
    [Total Movement Volume], 
    0 
)
```
- **Format**: `0.0%`

### Warehouse Channel Share %
```dax
Warehouse Channel Share % = 
DIVIDE ( 
    [Total Warehouse Sales Volume], 
    [Total Movement Volume], 
    0 
)
```
- **Format**: `0.0%`

### Average Retail Sales per Record
```dax
Average Retail Sales per Record = 
AVERAGE ( 'sales'[RETAIL SALES] )
```
- **Format**: `#,##0.00`

---

## 3. Catalog Breadth & Counts

### Distinct Products Count
```dax
Distinct Products Count = 
DISTINCTCOUNT ( 'sales'[ITEM CODE] )
```
- **Format**: `#,##0`

### Distinct Suppliers Count
```dax
Distinct Suppliers Count = 
DISTINCTCOUNT ( 'sales'[SUPPLIER] )
```
- **Format**: `#,##0`

### Distinct Item Types Count
```dax
Distinct Item Types Count = 
DISTINCTCOUNT ( 'sales'[ITEM TYPE] )
```
- **Format**: `0`

---

## 4. Time Intelligence & Year-over-Year (YoY)

### Retail Sales Prior Year
```dax
Retail Sales Prior Year = 
CALCULATE (
    [Total Retail Sales Volume],
    SAMEPERIODLASTYEAR ( 'Calendar'[Date] )
)
```
- **Format**: `#,##0.00`

### YoY Retail Sales Growth Volume
```dax
YoY Retail Sales Growth Volume = 
IF (
    NOT ISBLANK ( [Retail Sales Prior Year] ),
    [Total Retail Sales Volume] - [Retail Sales Prior Year],
    BLANK ()
)
```
- **Format**: `+#,##0.00;-#,##0.00;0.00`

### YoY Retail Sales Growth %
```dax
YoY Retail Sales Growth % = 
DIVIDE (
    [YoY Retail Sales Growth Volume],
    [Retail Sales Prior Year],
    BLANK ()
)
```
- **Format**: `+0.0%;-0.0%;0.0%`

---

## 5. Market Share & Pareto Analysis

### Retail Sales % of Total
```dax
Retail Sales % of Total = 
DIVIDE (
    [Total Retail Sales Volume],
    CALCULATE ( [Total Retail Sales Volume], ALLSELECTED ( 'sales' ) ),
    0
)
```
- **Format**: `0.00%`

### Cumulative Supplier Retail % (Pareto Line)
```dax
Cumulative Supplier Retail % = 
VAR CurrentSupplierSales = [Total Retail Sales Volume]
VAR AllSuppliers = 
    ADDCOLUMNS (
        ALLSELECTED ( 'sales'[SUPPLIER] ),
        "@Sales", [Total Retail Sales Volume]
    )
VAR RunningTotal = 
    SUMX (
        FILTER ( AllSuppliers, [@Sales] >= CurrentSupplierSales ),
        [@Sales]
    )
VAR TotalAllSuppliers = 
    SUMX ( AllSuppliers, [@Sales] )
RETURN
    DIVIDE ( RunningTotal, TotalAllSuppliers, 0 )
```
- **Format**: `0.0%`
- **Description**: Generates the cumulative percentage line for the top supplier Pareto chart.
