import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import lightgbm as lgb
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Ensure output directories exist
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
        print("Staging data not found. Generating synthetic data for LightGBM pipeline...")
        dates = pd.date_range(start="2011-01-29", periods=1000, freq='D')
        sales = np.random.normal(20000, 2000, 1000) + np.sin(np.arange(1000)*(2*np.pi/7))*3000
        df = pd.DataFrame({"date": dates, "total_units_sold": sales})
    
    df = df.sort_values('date').reset_index(drop=True)
    return df

def engineer_features(df):
    """
    Generate Lag, Rolling, Calendar, and Price features for LightGBM demand forecasting.
    """
    df = df.copy()
    
    # 1. Lag Features
    df['lag_1'] = df['total_units_sold'].shift(1)
    df['lag_7'] = df['total_units_sold'].shift(7)
    df['lag_14'] = df['total_units_sold'].shift(14)
    df['lag_28'] = df['total_units_sold'].shift(28)
    
    # 2. Rolling Statistics
    df['rolling_mean_7'] = df['total_units_sold'].shift(1).rolling(window=7).mean()
    df['rolling_mean_14'] = df['total_units_sold'].shift(1).rolling(window=14).mean()
    df['rolling_mean_30'] = df['total_units_sold'].shift(1).rolling(window=30).mean()
    df['rolling_std_7'] = df['total_units_sold'].shift(1).rolling(window=7).std()
    
    # 3. Calendar Features
    df['dayofweek'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month
    df['quarter'] = df['date'].dt.quarter
    df['is_weekend'] = df['dayofweek'].isin([5, 6]).astype(int)
    
    # US Holiday Flag simulation
    import holidays
    us_holidays = holidays.US(years=df['date'].dt.year.unique())
    df['is_holiday'] = df['date'].dt.date.isin(us_holidays).astype(int)
    
    # 4. Price & Promotional Features (simulated or extracted)
    np.random.seed(42)
    df['current_price'] = 19.99 + np.random.choice([0.0, -2.0, -5.0], size=len(df), p=[0.7, 0.2, 0.1])
    df['prev_price'] = df['current_price'].shift(1).fillna(19.99)
    df['discount_pct'] = ((df['prev_price'] - df['current_price']) / df['prev_price']).clip(lower=0) * 100
    
    return df

def train_lightgbm():
    print("Starting LightGBM Feature Engineering & Training Pipeline...")
    raw_df = load_data()
    df = engineer_features(raw_df)
    
    # Drop rows with NaN due to lag/rolling windows
    clean_df = df.dropna().reset_index(drop=True)
    
    feature_cols = [
        'lag_1', 'lag_7', 'lag_14', 'lag_28',
        'rolling_mean_7', 'rolling_mean_14', 'rolling_mean_30', 'rolling_std_7',
        'dayofweek', 'month', 'quarter', 'is_weekend', 'is_holiday',
        'current_price', 'prev_price', 'discount_pct'
    ]
    target_col = 'total_units_sold'
    
    # Split train/test (last 30 days for testing)
    train_df = clean_df.iloc[:-30]
    test_df = clean_df.iloc[-30:]
    
    X_train = train_df[feature_cols]
    y_train = train_df[target_col]
    X_test = test_df[feature_cols]
    y_test = test_df[target_col]
    
    # Configure LightGBM Regressor with hyperparameter tuning parameters
    model = lgb.LGBMRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=6,
        num_leaves=31,
        random_state=42,
        verbosity=-1
    )
    
    start_time = time.time()
    model.fit(X_train, y_train)
    training_time = time.time() - start_time
    
    # Predict test set (30 days)
    start_predict = time.time()
    predictions = model.predict(X_test)
    prediction_time = time.time() - start_predict
    
    actuals = y_test.values
    mae = mean_absolute_error(actuals, predictions)
    rmse = np.sqrt(mean_squared_error(actuals, predictions))
    mape = np.mean(np.abs((actuals - predictions) / actuals)) * 100
    
    print(f"LightGBM Training Time: {training_time:.2f}s")
    print(f"LightGBM MAE: {mae:.2f}")
    print(f"LightGBM RMSE: {rmse:.2f}")
    print(f"LightGBM MAPE: {mape:.2f}%")
    
    # Calculate confidence interval approximation based on residual std
    residuals = y_train - model.predict(X_train)
    std_residual = np.std(residuals)
    lower_bound = predictions - 1.96 * std_residual
    upper_bound = predictions + 1.96 * std_residual
    
    # Save predictions CSV
    forecast_df = pd.DataFrame({
        "ds": test_df['date'].values,
        "forecast_sales": predictions,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound
    })
    forecast_df.to_csv("data/processed/forecast_lightgbm.csv", index=False)
    
    # Store in SQLite database
    if os.path.exists("data/warehouse.db"):
        conn = sqlite3.connect("data/warehouse.db")
        forecast_df.to_sql("forecast_lightgbm", conn, if_exists="replace", index=False)
        conn.close()
        print("Stored LightGBM predictions to SQLite table `forecast_lightgbm`.")
        
    # 1. Feature Importance Plot
    importance_df = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': model.feature_importances_
    }).sort_values(by='Importance', ascending=True)
    
    plt.figure(figsize=(10, 6))
    plt.barh(importance_df['Feature'], importance_df['Importance'], color='teal')
    plt.title("LightGBM Feature Importance (Demand Forecasting)")
    plt.xlabel("Importance (Split Count)")
    plt.tight_layout()
    plt.savefig("reports/figures/feature_importance.png")
    plt.close()
    print("Saved feature importance chart to reports/figures/feature_importance.png")
    
    # 2. Forecast Visualization Plot
    plt.figure(figsize=(12, 6))
    plt.plot(clean_df['date'], clean_df['total_units_sold'], label='Historical Sales', color='black', alpha=0.6)
    plt.plot(test_df['date'], predictions, label='LightGBM Forecast', color='purple', linewidth=2)
    plt.fill_between(test_df['date'], lower_bound, upper_bound, color='purple', alpha=0.2, label='95% Confidence Interval')
    plt.axvline(x=test_df['date'].iloc[0], color='red', linestyle='--', label='Forecast Start')
    plt.title("LightGBM Retail Demand Forecast")
    plt.xlabel("Date")
    plt.ylabel("Units Sold")
    plt.legend()
    plt.tight_layout()
    plt.savefig("reports/figures/lightgbm_forecast.png")
    plt.close()
    print("Saved forecast plot to reports/figures/lightgbm_forecast.png")
    
    # Save execution metrics for comparison
    metrics = pd.DataFrame([{
        "model": "LightGBM",
        "mae": mae,
        "rmse": rmse,
        "mape": mape,
        "training_time": training_time,
        "prediction_time": prediction_time
    }])
    metrics.to_csv("data/processed/metrics_lightgbm.csv", index=False)
    print("LightGBM pipeline execution completed successfully.")

if __name__ == "__main__":
    train_lightgbm()
