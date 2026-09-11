# Power BI Data Model: Retail & Warehouse Sales Analytics

## Architecture Overview

The data model uses a Star-adjacent relational design optimized for Power BI's VertiPaq columnar in-memory storage engine.

```
       +----------------------------+
       |         Calendar           | (Dimension)
       +----------------------------+
       | Date (PK)                  |
       | Year                       |
       | Month Number               |
       | Month Name                 |
       | Year-Month (Key)           |
       | Year-Month Display         |
       +----------------------------+
                     | 1
                     |
                     | *
       +----------------------------+
       |           sales            | (Fact Table)
       +----------------------------+
       | YEAR                       |
       | MONTH                      |
       | SUPPLIER                   |
       | ITEM CODE                  |
       | ITEM DESCRIPTION           |
       | ITEM TYPE                  |
       | RETAIL SALES               |
       | RETAIL TRANSFERS           |
       | WAREHOUSE SALES            |
       | DateKey (Calculated)       |
       +----------------------------+
```

---

## 1. Fact Table: `sales`

- **Source File**: `data/cleaned_sales.csv` (307,642 rows)
- **Import Method**: Import Mode (Power Query)

### Column Dictionary

| Column Name | Power Query Type | Format String | Description |
|---|---|---|---|
| `YEAR` | Integer | `0` | Calendar year (2017 to 2020) |
| `MONTH` | Integer | `0` | Calendar month (1 to 12) |
| `SUPPLIER` | Text | Text | Primary brand vendor / manufacturer |
| `ITEM CODE` | Text | Text | Alphanumeric product SKU identifier |
| `ITEM DESCRIPTION` | Text | Text | Detailed product name and bottle size |
| `ITEM TYPE` | Text | Text | Product category (LIQUOR, WINE, BEER, etc.) |
| `RETAIL SALES` | Decimal Number | `#,##0.00` | Physical retail movement (cases / units) |
| `RETAIL TRANSFERS` | Decimal Number | `#,##0.00` | Inter-warehouse retail transfer volume |
| `WAREHOUSE SALES` | Decimal Number | `#,##0.00` | Wholesale warehouse distribution volume |

### Calculated Column for Relationship
In Power BI Desktop, add this column to `sales` to connect with `Calendar`:

```dax
DateKey = DATE ( 'sales'[YEAR], 'sales'[MONTH], 1 )
```

---

## 2. Dimension Table: `Calendar`

Generated using DAX to establish standard time intelligence.

### DAX Table Definition
```dax
Calendar = 
VAR MinYear = MIN ( 'sales'[YEAR] )
VAR MaxYear = MAX ( 'sales'[YEAR] )
RETURN
    ADDCOLUMNS (
        CALENDAR ( DATE ( MinYear, 1, 1 ), DATE ( MaxYear, 12, 31 ) ),
        "Year", YEAR ( [Date] ),
        "Month Number", MONTH ( [Date] ),
        "Month Name", FORMAT ( [Date], "MMMM" ),
        "Month Short", FORMAT ( [Date], "MMM" ),
        "Year-Month Key", YEAR ( [Date] ) * 100 + MONTH ( [Date] ),
        "Year-Month", FORMAT ( [Date], "YYYY-MM" )
    )
```

### Column Configuration in Power BI:
- Mark as Date Table: Set `[Date]` as primary date column.
- Sort `[Month Name]` by column `[Month Number]`.
- Sort `[Year-Month]` by column `[Year-Month Key]`.

---

## 3. Relationships

| From (Fact) | To (Dimension) | Cardinality | Cross Filter | Active |
|---|---|---|---|---|
| `'sales'[DateKey]` | `'Calendar'[Date]` | Many-to-One (`*:1`) | Single | Yes |

---

## 4. Modeling Best Practices

1. **Measure Isolation**: All DAX calculations are organized within a dedicated `_Measures` home table.
2. **Hidden Keys**: `DateKey` and `Year-Month Key` are hidden from report view to prevent user confusion.
3. **Column Summarization**: Set Default Summarization for `YEAR` and `MONTH` to **"Don't summarize"** so Power BI doesn't calculate sums of calendar years.
