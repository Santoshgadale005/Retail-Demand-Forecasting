"""
extract.py

Reads the raw M5 datasets from the data/raw folder.
"""

import pandas as pd


def load_data():
    """Load all raw datasets."""

    calendar = pd.read_csv("data/raw/calendar.csv")
    sales = pd.read_csv("data/raw/sales_train_validation.csv")
    prices = pd.read_csv("data/raw/sell_prices.csv")

    print("Datasets loaded successfully.")

    return calendar, sales, prices


if __name__ == "__main__":
    calendar, sales, prices = load_data()

    print("Calendar Shape:", calendar.shape)
    print("Sales Shape:", sales.shape)
    print("Prices Shape:", prices.shape)