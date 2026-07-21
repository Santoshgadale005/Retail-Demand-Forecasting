"""
load.py

Saves cleaned datasets into the data/processed folder.
"""

import os


def save_data(calendar, sales, prices):
    """Save cleaned datasets."""

    output_dir = "data/processed"

    os.makedirs(output_dir, exist_ok=True)

    calendar.to_csv(f"{output_dir}/calendar_clean.csv", index=False)
    sales.to_csv(f"{output_dir}/sales_clean.csv", index=False)
    prices.to_csv(f"{output_dir}/prices_clean.csv", index=False)

    print("Cleaned datasets saved successfully.")
    print(f"Files saved in: {output_dir}")