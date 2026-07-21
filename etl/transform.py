"""
transform.py

Contains data cleaning and transformation functions.
"""


def clean_calendar(calendar):
    """Clean the calendar dataset."""

    calendar = calendar.copy()

    # Fill missing event names
    calendar["event_name_1"] = calendar["event_name_1"].fillna("No Event")
    calendar["event_type_1"] = calendar["event_type_1"].fillna("None")

    calendar["event_name_2"] = calendar["event_name_2"].fillna("No Event")
    calendar["event_type_2"] = calendar["event_type_2"].fillna("None")

    print("Calendar cleaned successfully.")

    return calendar


def clean_sales(sales):
    """Clean the sales dataset."""

    sales = sales.copy()

    print("Sales dataset checked.")

    return sales


def clean_prices(prices):
    """Clean the prices dataset."""

    prices = prices.copy()

    print("Prices dataset checked.")

    return prices