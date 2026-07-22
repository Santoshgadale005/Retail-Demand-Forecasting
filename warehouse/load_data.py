"""
Load data into the warehouse.
"""

import sqlite3
import pandas as pd
from configs.config import DATA_DIR

DB_PATH = DATA_DIR / "warehouse.db"


def load_calendar():
    """Load calendar dimension."""

    conn = sqlite3.connect(DB_PATH)

    calendar = pd.read_csv(DATA_DIR / "processed" / "calendar_clean.csv")

    calendar = calendar[
        [
            "date",
            "weekday",
            "month",
            "year",
            "event_name_1",
            "event_type_1",
        ]
    ].rename(
        columns={
            "event_name_1": "event_name",
            "event_type_1": "event_type",
        }
    )

    calendar = calendar.drop_duplicates()
    conn.execute("DELETE FROM dim_calendar")
    calendar.to_sql(
        "dim_calendar",
        conn,
        if_exists="append",
        index=False,
    )

    conn.close()

    print("✅ dim_calendar loaded")


def load_item():
    """Load item dimension."""

    conn = sqlite3.connect(DB_PATH)

    sales = pd.read_csv(DATA_DIR / "processed" / "sales_clean.csv")

    items = (
        sales[
            [
                "item_id",
                "dept_id",
                "cat_id",
            ]
        ]
        .drop_duplicates()
        .rename(
            columns={
                "dept_id": "department",
                "cat_id": "category",
            }
        )
    )
    conn.execute("DELETE FROM dim_item")
    items.to_sql(
        "dim_item",
        conn,
        if_exists="append",
        index=False,
    )

    conn.close()

    print("✅ dim_item loaded")


def load_store():
    """Load store dimension."""

    conn = sqlite3.connect(DB_PATH)

    sales = pd.read_csv(DATA_DIR / "processed" / "sales_clean.csv")

    stores = (
        sales[
            [
                "store_id",
                "state_id",
            ]
        ]
        .drop_duplicates()
        .rename(
            columns={
                "state_id": "state",
            }
        )
    )
    conn.execute("DELETE FROM dim_store")
    stores.to_sql(
        "dim_store",
        conn,
        if_exists="append",
        index=False,
    )

    conn.close()

    print("✅ dim_store loaded")
    
def prepare_fact_sales():
    """Transform sales data from wide format to long format."""

    print("Loading sales data...")

    sales = pd.read_csv(
        DATA_DIR / "processed" / "sales_clean.csv"
    )

    print("Melting sales data...")

    # Select only daily sales columns
    sales_columns = [col for col in sales.columns if col.startswith("d_")]

    # Convert wide data to long format
    sales_long = sales.melt(
        id_vars=[
            "item_id",
            "dept_id",
            "cat_id",
            "store_id",
            "state_id",
        ],
        value_vars=sales_columns,
        var_name="d",
        value_name="sales_quantity",
    )

    # Load calendar
    calendar = pd.read_csv(
        DATA_DIR / "processed" / "calendar_clean.csv"
    )

    # Keep only mapping columns
    calendar = calendar[["d", "date"]]

    # Join sales with calendar
    sales_long = sales_long.merge(
        calendar,
        on="d",
        how="left"
    )

    print("\nAfter joining calendar:")
    print(sales_long[["d", "date", "sales_quantity"]].head())

    return sales_long
def load_fact_sales():
    """Load a sample of fact_sales into the warehouse."""

    conn = sqlite3.connect(DB_PATH)

    print("Preparing fact table...")

    sales_long = prepare_fact_sales()

    # Load prices
    prices = pd.read_csv(
        DATA_DIR / "processed" / "prices_clean.csv"
    )

    # Keep only required columns
    prices = prices[
        [
            "store_id",
            "item_id",
            "sell_price",
        ]
    ].drop_duplicates()

    # Join sales with prices
    fact_sales = sales_long.merge(
        prices,
        on=["item_id", "store_id"],
        how="left"
    )

    # Keep only warehouse columns
    fact_sales = fact_sales[
        [
            "date",
            "item_id",
            "store_id",
            "sales_quantity",
            "sell_price",
        ]
    ]

    # Development sample
    fact_sales = fact_sales.head(100000)

    # Clear existing data
    conn.execute("DELETE FROM fact_sales")

    # Load sample
    fact_sales.to_sql(
        "fact_sales",
        conn,
        if_exists="append",
        index=False,
    )

    conn.commit()
    conn.close()

    print(f"✅ Loaded {len(fact_sales)} rows into fact_sales")
    
if __name__ == "__main__":
    load_calendar()
    load_item()
    load_store()
    load_fact_sales()