"""
Project Configuration
=====================

Central configuration module for the Retail Demand Forecasting
& Inventory Optimization platform.

All project-wide settings, paths, and constants are defined here.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ===========================
# Path Configuration
# ===========================

PROJECT_ROOT = Path(__file__).parent.parent.resolve()

# Data paths
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

# Component paths
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
WAREHOUSE_DIR = PROJECT_ROOT / "warehouse"
DBT_DIR = PROJECT_ROOT / "dbt_project"
FORECASTING_DIR = PROJECT_ROOT / "forecasting"
INVENTORY_DIR = PROJECT_ROOT / "inventory"
STREAMLIT_DIR = PROJECT_ROOT / "streamlit"
REPORTS_DIR = PROJECT_ROOT / "reports"
TESTS_DIR = PROJECT_ROOT / "tests"
CONFIGS_DIR = PROJECT_ROOT / "configs"
LOGS_DIR = PROJECT_ROOT / "logs"

# ===========================
# Google Cloud Configuration
# ===========================

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
GCP_CREDENTIALS_PATH = os.getenv("GCP_CREDENTIALS_PATH", "")
BQ_DATASET = os.getenv("BQ_DATASET", "retail_forecasting")
BQ_LOCATION = os.getenv("BQ_LOCATION", "US")

# ===========================
# Kaggle Configuration
# ===========================

KAGGLE_DATASET = "m5-forecasting-accuracy"
KAGGLE_USERNAME = os.getenv("KAGGLE_USERNAME", "")
KAGGLE_KEY = os.getenv("KAGGLE_KEY", "")

# ===========================
# M5 Dataset File Names
# ===========================

M5_FILES = {
    "sales_train_validation": "sales_train_validation.csv",
    "sales_train_evaluation": "sales_train_evaluation.csv",
    "calendar": "calendar.csv",
    "sell_prices": "sell_prices.csv",
    "sample_submission": "sample_submission.csv",
}

# ===========================
# Forecasting Configuration
# ===========================

FORECAST_HORIZON = int(os.getenv("FORECAST_HORIZON", "28"))
TRAIN_TEST_SPLIT = float(os.getenv("TRAIN_TEST_SPLIT", "0.8"))

# Product hierarchy levels
HIERARCHY_LEVELS = [
    "total",       # All products across all stores
    "state",       # State-level aggregation (CA, TX, WI)
    "store",       # Store-level aggregation (CA_1, TX_1, etc.)
    "category",    # Category level (HOBBIES, HOUSEHOLD, FOODS)
    "department",  # Department level (HOBBIES_1, FOODS_1, etc.)
    "product",     # Individual product level
]

# Time series model configurations
PROPHET_CONFIG = {
    "changepoint_prior_scale": 0.05,
    "seasonality_prior_scale": 10.0,
    "holidays_prior_scale": 10.0,
    "seasonality_mode": "multiplicative",
    "yearly_seasonality": True,
    "weekly_seasonality": True,
    "daily_seasonality": False,
}

ARIMA_CONFIG = {
    "max_p": 5,
    "max_d": 2,
    "max_q": 5,
    "seasonal": True,
    "m": 7,  # Weekly seasonality
    "stepwise": True,
}

LIGHTGBM_CONFIG = {
    "objective": "regression",
    "metric": "rmse",
    "boosting_type": "gbdt",
    "num_leaves": 31,
    "learning_rate": 0.05,
    "feature_fraction": 0.9,
    "bagging_fraction": 0.8,
    "bagging_freq": 5,
    "n_estimators": 1000,
    "early_stopping_rounds": 50,
    "verbose": -1,
}

# ===========================
# Inventory Optimization
# ===========================

INVENTORY_CONFIG = {
    "service_level": 0.95,           # 95% service level
    "lead_time_days": 7,             # Average lead time
    "review_period_days": 7,         # Inventory review period
    "holding_cost_pct": 0.25,        # Annual holding cost (% of item cost)
    "ordering_cost": 50.0,           # Fixed ordering cost ($)
    "stockout_cost_multiplier": 2.0, # Stockout penalty multiplier
}

# ===========================
# Application Settings
# ===========================

APP_ENV = os.getenv("APP_ENV", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# ===========================
# BigQuery Table Names
# ===========================

BQ_TABLES = {
    # Raw layer
    "raw_sales": f"{BQ_DATASET}.raw_sales",
    "raw_calendar": f"{BQ_DATASET}.raw_calendar",
    "raw_prices": f"{BQ_DATASET}.raw_prices",
    # Staging layer (dbt)
    "stg_sales": f"{BQ_DATASET}.stg_sales",
    "stg_calendar": f"{BQ_DATASET}.stg_calendar",
    "stg_prices": f"{BQ_DATASET}.stg_prices",
    # Mart layer (dbt)
    "fact_sales": f"{BQ_DATASET}.fact_sales",
    "dim_product": f"{BQ_DATASET}.dim_product",
    "dim_store": f"{BQ_DATASET}.dim_store",
    "dim_date": f"{BQ_DATASET}.dim_date",
    # Forecast outputs
    "forecast_results": f"{BQ_DATASET}.forecast_results",
    "inventory_recommendations": f"{BQ_DATASET}.inventory_recommendations",
}
