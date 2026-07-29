import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Model Performance",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Model Performance Dashboard")

# -----------------------------
# Load Metrics
# -----------------------------
metrics_file = "reports/model_metrics.txt"

if os.path.exists(metrics_file):

    with open(metrics_file, "r") as f:
        lines = f.readlines()

    metrics = {}

    for line in lines:
        if ":" in line:
            key, value = line.split(":")
            metrics[key.strip()] = value.strip()

    col1, col2 = st.columns(2)

    with col1:
        st.metric("MAE", metrics.get("MAE", "N/A"))
        st.metric("MAPE", metrics.get("MAPE", "N/A"))

    with col2:
        st.metric("RMSE", metrics.get("RMSE", "N/A"))
        st.metric("R² Score", metrics.get("R²", "N/A"))

else:
    st.warning("model_metrics.txt not found.")

# -----------------------------
# Forecast Graph
# -----------------------------
st.subheader("Forecast vs Actual")

graph_path = "reports/forecast_vs_actual.png"

if os.path.exists(graph_path):
    st.image(graph_path, use_container_width=True)
else:
    st.warning("Forecast graph not found.")

# -----------------------------
# Predictions Table
# -----------------------------
st.subheader("Recent Predictions")

prediction_file = "reports/predictions.csv"

if os.path.exists(prediction_file):

    df = pd.read_csv(prediction_file)

    st.dataframe(df)

else:
    st.warning("predictions.csv not found.")