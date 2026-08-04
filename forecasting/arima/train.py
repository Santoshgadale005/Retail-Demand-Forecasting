import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Ensure outputs directories exist
os.makedirs("data/processed", exist_ok=True)
os.makedirs("reports/figures", exist_ok=True)

def load_data(data_path="data/processed/mart_daily_sales.csv"):
    """
    Loads daily sales. Fallback to generating synthetic data if CSV does not exist.
    """
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        df['date'] = pd.to_datetime(df['date'])
    else:
        print("Staging data not found. Generating synthetic data for ARIMA pipeline verification...")
        dates = pd.date_range(start="2011-01-29", periods=1000, freq='D')
        sales = np.random.normal(20000, 2000, 1000) + np.sin(np.arange(1000)*(2*np.pi/7))*3000
        df = pd.DataFrame({"date": dates, "total_units_sold": sales})
    
    df = df.sort_values('date').set_index('date')
    return df

def train_arima():
    df = load_data()
    
    # Split train/test (last 30 days for testing)
    train_series = df['total_units_sold'].iloc[:-30]
    test_series = df['total_units_sold'].iloc[-30:]
    
    # Configure and fit model
    # M5 has weekly seasonality (period=7). We fit a basic SARIMAX(1, 1, 1)x(1, 1, 1, 7) model
    model = SARIMAX(
        train_series,
        order=(1, 1, 1),
        seasonal_order=(1, 1, 1, 7),
        enforce_stationarity=False,
        enforce_invertibility=False
    )
    
    start_time = time.time()
    results = model.fit(disp=False)
    training_time = time.time() - start_time
    
    # Predict next 30 days
    start_predict = time.time()
    forecast_res = results.get_forecast(steps=30)
    prediction_time = time.time() - start_predict
    
    predicted_vals = forecast_res.predicted_mean
    conf_int = forecast_res.conf_int()
    
    # Evaluate performance on test set
    actuals = test_series.values
    predicted_vals_array = predicted_vals.values
    
    mae = mean_absolute_error(actuals, predicted_vals_array)
    rmse = np.sqrt(mean_squared_error(actuals, predicted_vals_array))
    mape = np.mean(np.abs((actuals - predicted_vals_array) / actuals)) * 100
    
    print(f"ARIMA Training Time: {training_time:.2f}s")
    print(f"ARIMA MAE: {mae:.2f}")
    print(f"ARIMA RMSE: {rmse:.2f}")
    print(f"ARIMA MAPE: {mape:.2f}%")
    
    # Save predictions
    forecast_df = pd.DataFrame({
        "ds": test_series.index,
        "forecast_sales": predicted_vals_array,
        "lower_bound": conf_int.iloc[:, 0].values,
        "upper_bound": conf_int.iloc[:, 1].values
    })
    forecast_df.to_csv("data/processed/forecast_arima.csv", index=False)
    
    # Visualize forecast
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['total_units_sold'], label='Historical Sales', color='black', alpha=0.6)
    plt.plot(predicted_vals.index, predicted_vals, label='ARIMA Forecast', color='green')
    plt.fill_between(predicted_vals.index, conf_int.iloc[:, 0], conf_int.iloc[:, 1], color='green', alpha=0.2, label='Confidence Interval')
    plt.axvline(x=test_series.index[0], color='red', linestyle='--', label='Forecast Start')
    plt.title("ARIMA/SARIMAX Demand Forecast")
    plt.xlabel("Date")
    plt.ylabel("Units Sold")
    plt.legend()
    plt.tight_layout()
    plt.savefig("reports/figures/arima_forecast.png")
    plt.close()
    
    # Save execution metrics for comparison
    metrics = pd.DataFrame([{
        "model": "ARIMA",
        "mae": mae,
        "rmse": rmse,
        "mape": mape,
        "training_time": training_time,
        "prediction_time": prediction_time
    }])
    metrics.to_csv("data/processed/metrics_arima.csv", index=False)
    print("ARIMA Forecast and Visualizations completed successfully.")

if __name__ == "__main__":
    train_arima()
