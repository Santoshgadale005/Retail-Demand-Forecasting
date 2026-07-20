import pandas as pd

# Load datasets
calendar = pd.read_csv("data/raw/calendar.csv")
sales = pd.read_csv("data/raw/sales_train_validation.csv")
prices = pd.read_csv("data/raw/sell_prices.csv")

print("=" * 50)
print("DATASET SHAPES")
print("=" * 50)
print("Calendar:", calendar.shape)
print("Sales:", sales.shape)
print("Prices:", prices.shape)

print("\n" + "=" * 50)
print("CALENDAR COLUMNS")
print("=" * 50)
print(calendar.columns.tolist())

print("\n" + "=" * 50)
print("SALES COLUMNS")
print("=" * 50)
print(sales.columns.tolist()[:10])  # First 10 columns

print("\n" + "=" * 50)
print("PRICES COLUMNS")
print("=" * 50)
print(prices.columns.tolist())

print("\n" + "=" * 50)
print("DATASET INFORMATION")
print("=" * 50)

print("\nCalendar Info")
calendar.info()

print("\nSales Info")
sales.info()

print("\nPrices Info")
prices.info()

print("\n" + "=" * 50)
print("MISSING VALUES")
print("=" * 50)

print("\nCalendar")
print(calendar.isnull().sum())

print("\nSales")
print(sales.isnull().sum())

print("\nPrices")
print(prices.isnull().sum())

print("\n" + "=" * 50)
print("DUPLICATE ROWS")
print("=" * 50)

print("Calendar:", calendar.duplicated().sum())
print("Sales:", sales.duplicated().sum())
print("Prices:", prices.duplicated().sum())

print("\n" + "=" * 50)
print("UNIQUE VALUES")
print("=" * 50)

print("Stores:", sales["store_id"].nunique())
print("Items:", sales["item_id"].nunique())
print("Departments:", sales["dept_id"].nunique())
print("Categories:", sales["cat_id"].nunique())
print("States:", sales["state_id"].nunique())