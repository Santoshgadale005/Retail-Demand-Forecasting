import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
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
        # Assuming table has date & total_units_sold
        df['date'] = pd.to_datetime(df['date'])
    else:
        print("Staging data not found. Generating synthetic data for Prophet pipeline verification...")
        dates = pd.date_range(start="2011-01-29", periods=1000, freq='D')
        sales = np.random.normal(20000, 2000, 1000) + np.sin(np.arange(1000)*(2*np.pi/7))*3000
        df = pd.DataFrame({"date": dates, "total_units_sold": sales})
    
    # Format for Prophet
    prophet_df = df.rename(columns={"date": "ds", "total_units_sold": "y"})
    return prophet_df

def train_prophet():
    df = load_data()
    
    # Split train/test (last 30 days for testing)
    train_df = df.iloc[:-30]
    test_df = df.iloc[-30:]
    
    # Configure and fit model
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False
    )
    
    # We can add holiday structures if needed. M5 has event_name columns.
    # In M5, holiday effects are significant. Let's add built-in US holidays.
    model.add_country_holidays(country_name='US')
    
    start_time = time.time()
    model.fit(train_df)
    training_time = time.time() - start_time
    
    # Predict future (last 30 days of train + 30 days of test = 30 days future forecast horizon)
    start_predict = time.time()
    future = model.make_future_dataframe(periods=30, freq='D')
    forecast = model.predict(future)
    prediction_time = time.time() - start_predict
    
    # Evaluate performance on test set
    predictions = forecast.iloc[-30:][['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    actuals = test_df['y'].values
    predicted_vals = predictions['yhat'].values
    
    mae = mean_absolute_error(actuals, predicted_vals)
    rmse = np.sqrt(mean_squared_error(actuals, predicted_vals))
    mape = np.mean(np.abs((actuals - predicted_vals) / actuals)) * 100
    
    print(f"Prophet Training Time: {training_time:.2f}s")
    print(f"Prophet MAE: {mae:.2f}")
    print(f"Prophet RMSE: {rmse:.2f}")
    print(f"Prophet MAPE: {mape:.2f}%")
    
    # Save predictions
    forecast_results = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].rename(
        columns={"yhat": "forecast_sales", "yhat_lower": "lower_bound", "yhat_upper": "upper_bound"}
    )
    forecast_results.to_csv("data/processed/forecast_prophet.csv", index=False)
    
    # Visualize forecast
    plt.figure(figsize=(12, 6))
    plt.plot(df['ds'], df['y'], label='Historical Sales', color='black', alpha=0.6)
    plt.plot(forecast['ds'], forecast['yhat'], label='Prophet Forecast', color='blue')
    plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='blue', alpha=0.2, label='Confidence Interval')
    plt.axvline(x=test_df['ds'].iloc[0], color='red', linestyle='--', label='Forecast Start')
    plt.title("Facebook Prophet Demand Forecast")
    plt.xlabel("Date")
    plt.ylabel("Units Sold")
    plt.legend()
    plt.tight_layout()
    plt.savefig("reports/figures/prophet_forecast.png")
    plt.close()
    
    # Save execution metrics for comparison
    metrics = pd.DataFrame([{
        "model": "Prophet",
        "mae": mae,
        "rmse": rmse,
        "mape": mape,
        "training_time": training_time,
        "prediction_time": prediction_time
    }])
    metrics.to_csv("data/processed/metrics_prophet.csv", index=False)
    print("Prophet Forecast and Visualizations completed successfully.")

if __name__ == "__main__":
    train_prophet()
