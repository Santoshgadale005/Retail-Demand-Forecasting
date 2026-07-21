"""
data_quality.py

Performs basic data quality checks on the processed datasets.
"""

import pandas as pd


def check_dataset(name, df):
    print("=" * 50)
    print(f"{name} Dataset")
    print("=" * 50)

    print("Shape:", df.shape)
    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:", df.duplicated().sum())

    print("\nData Types:")
    print(df.dtypes)

    print("\n")


calendar = pd.read_csv("data/processed/calendar_clean.csv")
sales = pd.read_csv("data/processed/sales_clean.csv")
prices = pd.read_csv("data/processed/prices_clean.csv")

check_dataset("Calendar", calendar)
check_dataset("Sales", sales)
check_dataset("Prices", prices)

print("=" * 50)
print("Data Quality Validation Completed Successfully!")
print("=" * 50)