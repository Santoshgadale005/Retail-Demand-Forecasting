import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

from preprocess import load_sales_data, create_daily_sales, create_features


def train_model():

    # Load data
    sales = load_sales_data()

    daily_sales = create_daily_sales(sales)

    df = create_features(daily_sales)

    # Features
    X = df[
        [
            "day_number",
            "lag_1",
            "lag_7",
            "lag_28",
            "rolling_mean_7",
            "rolling_mean_28",
        ]
    ]

    # Target
    y = df["sales"]

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    # Train Model
    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    # Evaluation
    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)

    print("=" * 50)
    print("Model Performance")
    print("=" * 50)

    print(f"MAE  : {mae:.2f}")
    print(f"RMSE : {rmse:.2f}")
    print(f"R2   : {r2:.4f}")

    # Save Model
    joblib.dump(model, "models/demand_forecasting.pkl")

    print("\nModel saved successfully!")


if __name__ == "__main__":
    train_model()