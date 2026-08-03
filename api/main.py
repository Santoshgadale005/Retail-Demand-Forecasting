from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator
import sqlite3
import pandas as pd
import logging
import joblib
import os

app = FastAPI(
    title="Retail Demand Forecasting API",
    description="REST API for Retail Demand Forecasting Project",
    version="1.0.0"
)
Instrumentator().instrument(app).expose(app)

DATABASE = "data/warehouse.db"
MODEL_PATH = "models/demand_forecasting.pkl"
logging.basicConfig(
    filename="logs/api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True
)
logging.info("===== API STARTED SUCCESSFULLY =====")


def get_connection():
    return sqlite3.connect(DATABASE)


@app.get("/")
def home():
    return {
        "message": "Retail Demand Forecasting API is running successfully!"
    }
@app.get("/health")
def health():
    db_status = "Connected"

    try:
        conn = sqlite3.connect(DATABASE)
        conn.close()
    except Exception:
        db_status = "Disconnected"

    return {
        "status": "Healthy",
        "database": db_status,
        "model": "Available" if os.path.exists(MODEL_PATH) else "Not Found"
    }

@app.get("/sales")
def sales_summary():
    conn = get_connection()

    df = pd.read_sql(
        "SELECT * FROM fact_sales",
        conn
    )

    conn.close()

    return {
        "total_sales": int(df["sales_quantity"].sum()),
        "average_sales": round(df["sales_quantity"].mean(), 2),
        "stores": int(df["store_id"].nunique()),
        "products": int(df["item_id"].nunique())
    }


@app.get("/inventory")
def inventory():
    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT item_id,
               SUM(sales_quantity) AS stock
        FROM fact_sales
        GROUP BY item_id
        ORDER BY stock DESC
        LIMIT 20
        """,
        conn
    )

    conn.close()

    return df.to_dict(orient="records")


@app.get("/forecast")
def forecast():
    if not os.path.exists(MODEL_PATH):
        return {"error": "Model not found"}

    return {
        "forecasted_sales": 12673.20
    }


class PredictionInput(BaseModel):
    lag_1: float
    lag_7: float
    lag_28: float
    rolling_mean_7: float
    rolling_mean_28: float
    day_number: int

@app.post("/predict")
def predict(data: PredictionInput):

    logging.info("Prediction request received")

    if not os.path.exists(MODEL_PATH):
        logging.error("Model file not found.")
        return {"error": "Model file not found."}

    model = joblib.load(MODEL_PATH)

    features = pd.DataFrame([{
        "day_number": data.day_number,
        "lag_1": data.lag_1,
        "lag_7": data.lag_7,
        "lag_28": data.lag_28,
        "rolling_mean_7": data.rolling_mean_7,
        "rolling_mean_28": data.rolling_mean_28
    }])

    prediction = model.predict(features)[0]

    logging.info(f"Prediction generated: {round(float(prediction), 2)}")

    return {
        "predicted_sales": round(float(prediction), 2)
    }