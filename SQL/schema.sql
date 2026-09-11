-- ================================================================
-- schema.sql
-- Retail & Warehouse Sales Analytics — SQLite schema
-- ================================================================
-- Single fact-style table holding the cleaned dataset.
-- Kept as one flat table (rather than a normalized star schema)
-- because the source data has no separate dimension keys beyond
-- ITEM CODE, and a single table keeps this portfolio project easy
-- to run end-to-end in SQLite with zero setup.
-- ================================================================

DROP TABLE IF EXISTS sales;

CREATE TABLE sales (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    year              INTEGER NOT NULL,
    month             INTEGER NOT NULL,
    supplier          TEXT NOT NULL,
    item_code         TEXT NOT NULL,
    item_description  TEXT NOT NULL,
    item_type         TEXT NOT NULL,
    retail_sales      REAL NOT NULL,
    retail_transfers  REAL NOT NULL,
    warehouse_sales   REAL NOT NULL
);

CREATE INDEX idx_sales_year_month ON sales (year, month);
CREATE INDEX idx_sales_supplier   ON sales (supplier);
CREATE INDEX idx_sales_item_type  ON sales (item_type);
CREATE INDEX idx_sales_item_desc  ON sales (item_description);