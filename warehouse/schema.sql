-- ==========================================
-- Retail Demand Forecasting Data Warehouse
-- Star Schema
-- ==========================================

-- ===========================
-- Dimension Table: Calendar
-- ===========================
CREATE TABLE IF NOT EXISTS dim_calendar (
    date TEXT PRIMARY KEY,
    weekday TEXT,
    month INTEGER,
    year INTEGER,
    event_name TEXT,
    event_type TEXT
);

-- ===========================
-- Dimension Table: Item
-- ===========================
CREATE TABLE IF NOT EXISTS dim_item (
    item_id TEXT PRIMARY KEY,
    department TEXT,
    category TEXT
);

-- ===========================
-- Dimension Table: Store
-- ===========================
CREATE TABLE IF NOT EXISTS dim_store (
    store_id TEXT PRIMARY KEY,
    state TEXT
);

-- ===========================
-- Fact Table: Sales
-- ===========================
CREATE TABLE IF NOT EXISTS fact_sales (
    date TEXT,
    item_id TEXT,
    store_id TEXT,
    sales_quantity INTEGER,
    sell_price REAL,
    FOREIGN KEY (date) REFERENCES dim_calendar(date),
    FOREIGN KEY (item_id) REFERENCES dim_item(item_id),
    FOREIGN KEY (store_id) REFERENCES dim_store(store_id)
);