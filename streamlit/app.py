import streamlit as st
import sqlite3
import pandas as pd

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Retail Demand Forecasting Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Retail Demand Forecasting Dashboard")
st.markdown("### Real-Time Retail Analytics & Demand Forecasting")

# ---------------------------------------------------
# Connect to SQLite Database
# ---------------------------------------------------
try:
    conn = sqlite3.connect("data/warehouse.db")

    sales_df = pd.read_sql(
        "SELECT * FROM fact_sales",
        conn
    )

except Exception as e:
    st.error(f"Database Connection Failed\n\n{e}")
    st.stop()

# ---------------------------------------------------
# Data Preparation
# ---------------------------------------------------
sales_df["date"] = pd.to_datetime(sales_df["date"])

# ---------------------------------------------------
# KPI Calculations
# ---------------------------------------------------
total_sales = int(sales_df["sales_quantity"].sum())

average_sales = round(
    sales_df["sales_quantity"].mean(),
    2
)

total_products = sales_df["item_id"].nunique()

total_stores = sales_df["store_id"].nunique()

# ---------------------------------------------------
# KPI Cards
# ---------------------------------------------------
st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Sales",
        f"{total_sales:,}"
    )

with col2:
    st.metric(
        "Average Sales",
        average_sales
    )

with col3:
    st.metric(
        "Products",
        total_products
    )

with col4:
    st.metric(
        "Stores",
        total_stores
    )

# ---------------------------------------------------
# Daily Sales Trend
# ---------------------------------------------------
st.divider()

st.subheader("📈 Daily Sales Trend")

daily_sales = (
    sales_df
    .groupby("date")["sales_quantity"]
    .sum()
    .reset_index()
)

st.line_chart(
    daily_sales.set_index("date")
)

# ---------------------------------------------------
# Top Selling Products
# ---------------------------------------------------
st.divider()

st.subheader("🏆 Top 10 Selling Products")

top_products = (
    sales_df
    .groupby("item_id")["sales_quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_products)

# ---------------------------------------------------
# Inventory Summary
# ---------------------------------------------------
st.divider()

st.subheader("📦 Inventory Summary")

inventory = (
    sales_df
    .groupby("item_id")["sales_quantity"]
    .sum()
    .reset_index()
)

inventory.columns = [
    "Product",
    "Stock"
]

st.dataframe(
    inventory.head(20),
    use_container_width=True
)

# ---------------------------------------------------
# Dashboard Modules
# ---------------------------------------------------
st.divider()

st.subheader("📌 Dashboard Modules")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
### 📈 Sales Overview

- Daily Sales Trends
- Revenue Analysis
- Product Performance
- Store Performance
""")

with col2:
    st.success("""
### 🔮 Demand Forecast

- Demand Prediction
- Forecast Analytics
- Trend Monitoring
- Future Planning
""")

with col3:
    st.warning("""
### 📦 Inventory Dashboard

- Current Inventory
- Low Stock Monitoring
- Product Availability
- Inventory Reports
""")

# ---------------------------------------------------
# Recent Sales Records
# ---------------------------------------------------
st.divider()

st.subheader("🗂 Recent Sales Data")

st.dataframe(
    sales_df.head(20),
    use_container_width=True
)

# ---------------------------------------------------
# Footer
# ---------------------------------------------------
st.divider()

st.success("✅ Dashboard Loaded Successfully")

st.caption(
    "Retail Demand Forecasting System | Day 13 | Streamlit Dashboard"
)