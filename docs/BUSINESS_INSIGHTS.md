# Business & Operational Insights: Retail & Warehouse Sales Analytics

## Executive Summary

Analysis of **307,642 transaction records** spanning 2017 through 2020 across county-operated liquor control operations reveals critical insights into channel dynamics, product mix disparities, supplier concentration, and temporal volatility.

All findings are grounded strictly in **physical movement volume** (cases and units), avoiding speculative monetary assumptions.

---

## 1. Wholesale Dominance vs Retail Footprint

Across total recorded logistics movement (12.08M units):
- **Warehouse Wholesale Distribution**: **7,781,756.28 units** (**64.4%** of total movement)
- **Retail Store Sales**: **2,160,899.37 units** (**17.9%** of total movement)
- **Retail Inter-Facility Transfers**: **2,133,968.63 units** (**17.7%** of total movement)

### Strategic Takeaways:
1. **Logistical Multiplier**: For every 1 case sold in retail stores, the central warehouse distributes ~3.6 cases to commercial licensees (bars, restaurants, independent wine/beer outlets). The business is primarily a wholesale distribution operation.
2. **Replenishment Coupling**: Retail sales and retail transfers demonstrate a **0.9601 Pearson correlation coefficient**. Inter-facility transfers closely track retail demand with near-zero inventory float.

---

## 2. Category Channel Divergence (Beer vs Liquor vs Wine)

Product categories behave fundamentally differently between retail and wholesale channels:

```
+---------------+------------------------+---------------------------+
| Category      | Retail Volume Share    | Warehouse Volume Share    |
+---------------+------------------------+---------------------------+
| LIQUOR        | 37.15% (802,691 units) |  1.22% (94,906 units)     |
| WINE          | 34.55% (746,498 units) | 14.87% (1,156,985 units)  |
| BEER          | 26.57% (574,220 units) | 83.88% (6,527,237 units)  |
| NON-ALCOHOL   |  1.58% (34,084 units)  |  0.34% (26,150 units)     |
+---------------+------------------------+---------------------------+
```

### Strategic Takeaways:
1. **Beer is Wholesale-Driven**: Beer accounts for **83.88% of all warehouse volume**, driven by high-velocity keg and case shipments to commercial hospitality accounts. In retail stores, beer represents only 26.57% of volume.
2. **Liquor is Retail-Centric**: Liquor is the single largest retail category (**37.15%** of store volume), but represents only 1.22% of warehouse shipments, reflecting county retail exclusivity for distilled spirits.
3. **Wine Balances Both Channels**: Wine represents ~35% of retail and ~15% of wholesale volume, requiring dual-channel logistics coordination.

---

## 3. High Supplier Concentration (Pareto Principle)

Out of **397 distinct suppliers** in the catalog:
- **Top 10 Suppliers** account for **1,022,192.37 units** (**47.30%** of total retail volume).
- **Top 20 Suppliers** account for **1,466,699.41 units** (**67.87%** of total retail volume).
- The remaining 377 suppliers share less than one-third of the retail market.

### Top 5 Volume Drivers:
1. **E & J GALLO WINERY**: 166,170.53 units (7.69% share) — Market leader in wine.
2. **DIAGEO NORTH AMERICA INC**: 145,343.20 units (6.73% share) — Market leader in spirits.
3. **CONSTELLATION BRANDS**: 131,664.79 units (6.09% share) — Major beer & wine importer.
4. **ANHEUSER BUSCH INC**: 109,960.82 units (5.09% share) — Domestic beer volume leader.
5. **JIM BEAM BRANDS CO**: 96,164.04 units (4.45% share) — Bourbon/spirits staple.

### Strategic Takeaways:
Vendor management and delivery service-level agreements (SLAs) should focus heavily on the top 20 suppliers to mitigate out-of-stock risk on nearly 70% of store sales.

---

## 4. SKU Pareto & Leading Products

The product catalog contains **34,820 distinct SKUs**. However, the **Top 10 SKUs** account for **148,430.58 units** (**6.87%** of total retail volume).

### Top 5 SKUs by Retail Volume:
1. `TITO'S HANDMADE VODKA - 1.75L`: **27,580.50 units** (1.28% of entire retail volume) — Single highest volume SKU.
2. `CORONA EXTRA LOOSE NR - 12OZ`: **25,064.00 units** (1.16%)
3. `HEINEKEN LOOSE NR - 12OZ`: **17,761.00 units** (0.82%)
4. `MILLER LITE 30PK CAN - 12OZ`: **14,440.00 units** (0.67%)
5. `BUD LIGHT 30PK CAN`: **12,299.00 units** (0.57%)

### Strategic Takeaways:
Large-format spirits (1.75L Tito's) and bulk/loose beer packs (30-packs and 12oz loose) drive the highest shelf turnover. Dedicated pallet and end-cap space should prioritize these top SKUs.

---

## 5. Temporal Patterns & Shock Events

Across the 24 active calendar months:

### Seasonal Peaks & Troughs
- **Holiday Peak**: December 2017 recorded the highest monthly retail volume (**131,634.49 units**), representing a **35.6% surge** over the 2017 monthly baseline.
- **Post-Holiday Trough**: January consistently registers the annual volume low across every recorded year:
  - January 2018: 75,791.77 units
  - January 2019: 76,100.53 units
  - January 2020: 74,318.77 units (all-time monthly low)
  This indicates a recurring ~40% drop between December peak and January post-holiday demand.

### The Pandemic Demand Surge (March 2020)
In March 2020, retail store volume spiked to **109,411.29 units**, the second-highest month in the entire 4-year dataset. This reflects consumer "pantry-loading" immediately preceding COVID-19 hospitality closures and restrictions.
