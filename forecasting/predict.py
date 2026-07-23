import joblib
import pandas as pd

# Load the trained model
model = joblib.load("models/demand_forecasting.pkl")

# Sample input
sample = pd.DataFrame(
    {
        "day_number": [1914],
        "lag_1": [25000],
        "lag_7": [24500],
        "lag_28": [24000],
        "rolling_mean_7": [24800],
        "rolling_mean_28": [24200],
    }
)

# Predict
prediction = model.predict(sample)

print("=" * 50)
print("Demand Forecast")
print("=" * 50)
print(f"Predicted Sales: {prediction[0]:.2f}")