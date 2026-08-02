import os
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# Ensure reports directory exists for saving output figures
REPORTS_DIR = "reports/figures"
os.makedirs(REPORTS_DIR, exist_ok=True)

def perform_eda(data_path="data/processed/mart_daily_sales.csv"):
    """
    Perform Time-Series Exploratory Data Analysis (EDA) on daily sales.
    If BigQuery isn't live, this uses the locally processed data or a dummy dataset.
    """
    print(f"Starting Time-Series EDA from {data_path}...")
    
    # Check if data exists, else mock for the EDA pipeline demonstration
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
    else:
        print("Real data not found. Generating dummy dataset for EDA pipeline testing...")
        dates = pd.date_range(start="2011-01-29", periods=1000, freq='D')
        import numpy as np
        sales = np.random.normal(500, 50, 1000) + np.sin(np.arange(1000)*(2*np.pi/365))*100
        df = pd.DataFrame({"date": dates, "total_units_sold": sales})

    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').set_index('date')
    
    # 1. Plot Sales Trends
    plt.figure(figsize=(14, 6))
    plt.plot(df.index, df['total_units_sold'], label="Daily Sales", color='blue', alpha=0.7)
    plt.title("Daily Total Units Sold (Trend & Seasonality)")
    plt.xlabel("Date")
    plt.ylabel("Units Sold")
    plt.legend()
    plt.savefig(f"{REPORTS_DIR}/daily_sales_trend.png")
    plt.close()
    print(f"Saved trend plot to {REPORTS_DIR}/daily_sales_trend.png")

    # 2. Test Stationarity (Augmented Dickey-Fuller)
    print("\nRunning Augmented Dickey-Fuller (ADF) Test...")
    result = adfuller(df['total_units_sold'].dropna())
    print(f"ADF Statistic: {result[0]}")
    print(f"p-value: {result[1]}")
    if result[1] <= 0.05:
        print("Result: Strong evidence against the null hypothesis (Stationary).")
    else:
        print("Result: Weak evidence against the null hypothesis (Non-Stationary).")

    # 3. Explore Autocorrelation (ACF / PACF)
    fig, axes = plt.subplots(1, 2, figsize=(16, 5))
    plot_acf(df['total_units_sold'].dropna(), lags=40, ax=axes[0])
    plot_pacf(df['total_units_sold'].dropna(), lags=40, ax=axes[1])
    plt.savefig(f"{REPORTS_DIR}/acf_pacf_plots.png")
    plt.close()
    print(f"Saved ACF/PACF plots to {REPORTS_DIR}/acf_pacf_plots.png")
    
    print("\nTime-Series EDA Completed successfully!")

if __name__ == "__main__":
    perform_eda()
