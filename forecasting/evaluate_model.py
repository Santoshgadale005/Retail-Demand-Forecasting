import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

# -----------------------------
# Connect to Warehouse Database
# -----------------------------
conn = sqlite3.connect("data/warehouse.db")

# Load sales data
query = """
SELECT date, sales_quantity
FROM fact_sales
ORDER BY date
"""

df = pd.read_sql(query, conn)
conn.close()


# -----------------------------
# Aggregate Daily Sales
# -----------------------------
daily_sales = (
    df.groupby("date")["sales_quantity"]
    .sum()
    .reset_index()
)
print("\nDaily Sales Shape:", daily_sales.shape)
print(daily_sales.head(10))
print(daily_sales.tail(10))

# -----------------------------
# Simple Forecast
# -----------------------------
daily_sales["forecast"] = (
    daily_sales["sales_quantity"]
    .rolling(window=7)
    .mean()
)

daily_sales.dropna(inplace=True)

# -----------------------------
# Evaluation Metrics
# -----------------------------
actual = daily_sales["sales_quantity"]
predicted = daily_sales["forecast"]

# --------------------------------
# Save Predictions
# --------------------------------

predictions = daily_sales[
    ["date", "sales_quantity", "forecast"]
].copy()

predictions.columns = [
    "Date",
    "Actual",
    "Forecast"
]

predictions.to_csv(
    "reports/predictions.csv",
    index=False
)

print("✅ Predictions saved to reports/predictions.csv")

mae = mean_absolute_error(actual, predicted)
rmse = np.sqrt(mean_squared_error(actual, predicted))
mape = np.mean(np.abs((actual - predicted) / actual)) * 100
r2 = r2_score(actual, predicted)

# -----------------------------
# Print Results
# -----------------------------
print("=" * 40)
print("MODEL PERFORMANCE")
print("=" * 40)

print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"MAPE : {mape:.2f}%")
print(f"R²   : {r2:.4f}")

# Save metrics to a file
with open("reports/model_metrics.txt", "w") as f:
    f.write("MODEL PERFORMANCE\n")
    f.write("=========================\n")
    f.write(f"MAE  : {mae:.2f}\n")
    f.write(f"RMSE : {rmse:.2f}\n")
    f.write(f"MAPE : {mape:.2f}%\n")
    f.write(f"R²   : {r2:.4f}\n")

print("\n✅ Metrics saved to reports/model_metrics.txt")

plt.figure(figsize=(10, 5))

plt.plot(
    predictions["Date"],
    predictions["Actual"],
    marker="o",
    label="Actual Sales"
)

plt.plot(
    predictions["Date"],
    predictions["Forecast"],
    marker="o",
    label="Forecast"
)

plt.title("Forecast vs Actual Sales")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

plt.savefig("reports/forecast_vs_actual.png")

print("✅ Forecast graph saved to reports/forecast_vs_actual.png")