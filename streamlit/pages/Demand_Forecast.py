import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import numpy as np

# -----------------------------------
# Page Configuration
# -----------------------------------
st.set_page_config(
    page_title="Demand Forecast",
    page_icon="🔮",
    layout="wide"
)

st.title("🔮 Demand Forecast Dashboard")

# -----------------------------------
# Load Data
# -----------------------------------
try:
    conn = sqlite3.connect("data/warehouse.db")

    query = """
    SELECT
        date,
        sales_quantity
    FROM fact_sales
    ORDER BY date;
    """

    df = pd.read_sql(query, conn)
    conn.close()

    st.success("✅ Demand forecast data loaded successfully!")

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# -----------------------------------
# Prepare Data
# -----------------------------------
daily_sales = (
    df.groupby("date")["sales_quantity"]
      .sum()
      .reset_index()
)

daily_sales["date"] = pd.to_datetime(daily_sales["date"])

# -----------------------------------
# Sidebar Filter
# -----------------------------------
st.sidebar.header("🔍 Filters")

min_date = daily_sales["date"].min()
max_date = daily_sales["date"].max()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(selected_dates) == 2:
    start_date, end_date = selected_dates
    daily_sales = daily_sales[
        (daily_sales["date"] >= pd.to_datetime(start_date)) &
        (daily_sales["date"] <= pd.to_datetime(end_date))
    ]

# -----------------------------------
# Forecast (7-Day Moving Average)
# -----------------------------------
daily_sales["Predicted Sales"] = (
    daily_sales["sales_quantity"]
    .rolling(window=7, min_periods=1)
    .mean()
)

daily_sales["Error"] = (
    daily_sales["sales_quantity"] -
    daily_sales["Predicted Sales"]
)

daily_sales["Absolute Error"] = daily_sales["Error"].abs()

daily_sales["APE"] = np.where(
    daily_sales["sales_quantity"] == 0,
    0,
    (daily_sales["Absolute Error"] /
     daily_sales["sales_quantity"]) * 100
)

mape = daily_sales["APE"].mean()

# -----------------------------------
# KPI Cards
# -----------------------------------
total_days = len(daily_sales)
avg_sales = daily_sales["sales_quantity"].mean()
latest_prediction = daily_sales["Predicted Sales"].iloc[-1]
total_sales = daily_sales["sales_quantity"].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Days", total_days)

with col2:
    st.metric("Total Sales", f"{int(total_sales):,}")

with col3:
    st.metric("Average Daily Sales", f"{avg_sales:.2f}")

with col4:
    st.metric("Latest Forecast", f"{latest_prediction:.2f}")

st.divider()

# -----------------------------------
# Actual vs Forecast
# -----------------------------------
st.subheader("📈 Actual vs Forecast")

fig = px.line(
    daily_sales,
    x="date",
    y=["sales_quantity", "Predicted Sales"],
    labels={
        "value": "Sales",
        "variable": "Legend"
    },
    title="Actual Sales vs Forecast"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# Forecast Error
# -----------------------------------
st.subheader("📉 Forecast Error")

fig2 = px.bar(
    daily_sales,
    x="date",
    y="Error",
    title="Forecast Error"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------------
# Forecast Accuracy
# -----------------------------------
st.subheader("🎯 Forecast Accuracy")

accuracy = max(0, 100 - mape)

col1, col2 = st.columns(2)

with col1:
    st.metric("MAPE", f"{mape:.2f}%")

with col2:
    st.metric("Forecast Accuracy", f"{accuracy:.2f}%")

# -----------------------------------
# Forecast Table
# -----------------------------------
st.subheader("📋 Last 30 Forecast Records")

st.dataframe(
    daily_sales.tail(30),
    use_container_width=True
)

# -----------------------------------
# Summary Statistics
# -----------------------------------
st.subheader("📊 Summary Statistics")

st.dataframe(
    daily_sales.describe(),
    use_container_width=True
)

# -----------------------------------
# Executive Summary
# -----------------------------------
st.divider()

st.info("""
### 📌 Dashboard Features

- ✅ Date Range Filter
- ✅ Forecast KPI Cards
- ✅ Actual vs Forecast Comparison
- ✅ Forecast Error Analysis
- ✅ Forecast Accuracy (MAPE)
- ✅ 30-Day Forecast Table
- ✅ Summary Statistics
- ✅ Executive Dashboard
""")