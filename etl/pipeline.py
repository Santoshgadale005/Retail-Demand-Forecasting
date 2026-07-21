"""
pipeline.py

Main ETL pipeline.
"""

from extract import load_data
from transform import clean_calendar, clean_sales, clean_prices
from load import save_data


def run_pipeline():

    print("=" * 50)
    print("Starting ETL Pipeline")
    print("=" * 50)

    # Extract
    calendar, sales, prices = load_data()

    # Transform
    calendar = clean_calendar(calendar)
    sales = clean_sales(sales)
    prices = clean_prices(prices)

    # Load
    save_data(calendar, sales, prices)

    print("=" * 50)
    print("ETL Pipeline Completed Successfully!")
    print("=" * 50)


if __name__ == "__main__":
    run_pipeline()