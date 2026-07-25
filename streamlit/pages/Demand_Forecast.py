import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Demand Forecast",
    page_icon="📈",
    layout="wide"
)

st.title("🔮 Demand Forecast Dashboard")

# -----------------------------
# Load Data
# -----------------------------
try:
    conn = sqlite3.connect("data/warehouse.db")

    query = """
    SELECT date, sales_quantity
    FROM fact_sales
    ORDER BY date
    """

    df = pd.read_sql(query, conn)
    conn.close()

    st.success("Data Loaded Successfully!")

except Exception as e:
    st.error(e)
    st.stop()

# -----------------------------
# Aggregate Daily Sales
# -----------------------------
daily_sales = (
    df.groupby("date")["sales_quantity"]
      .sum()
      .reset_index()
)

# -----------------------------
# Simple Forecast
# -----------------------------
daily_sales["Predicted Sales"] = (
    daily_sales["sales_quantity"]
    .rolling(window=7)
    .mean()
)

daily_sales["Predicted Sales"].fillna(
    daily_sales["sales_quantity"],
    inplace=True
)

# -----------------------------
# KPI Cards
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Days",
        len(daily_sales)
    )

with col2:
    st.metric(
        "Average Daily Sales",
        round(daily_sales["sales_quantity"].mean(),2)
    )

with col3:
    st.metric(
        "Latest Prediction",
        round(daily_sales["Predicted Sales"].iloc[-1],2)
    )

st.divider()

# -----------------------------
# Actual vs Predicted
# -----------------------------
st.subheader("📈 Actual vs Predicted Sales")

fig = px.line(
    daily_sales,
    x="date",
    y=["sales_quantity","Predicted Sales"],
    labels={
        "value":"Sales",
        "variable":"Legend"
    }
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Forecast Table
# -----------------------------
st.subheader("Forecast Data")

st.dataframe(
    daily_sales.tail(30)
)

# -----------------------------
# Prediction Error
# -----------------------------
daily_sales["Error"] = (
    daily_sales["sales_quantity"] -
    daily_sales["Predicted Sales"]
)

st.subheader("Prediction Error")

fig2 = px.bar(
    daily_sales.tail(30),
    x="date",
    y="Error"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Summary
# -----------------------------
st.info("""
### Dashboard Summary

- Actual Daily Sales
- Rolling Forecast
- Prediction Error
- Latest 30-Day Forecast
""")