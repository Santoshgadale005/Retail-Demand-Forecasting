import streamlit as st
import pandas as pd
import sqlite3

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Sales Overview",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Sales Overview Dashboard")

# -----------------------------
# Load Data from SQLite
# -----------------------------
try:
    conn = sqlite3.connect("data/warehouse.db")

    query = """
    SELECT *
    FROM fact_sales
    LIMIT 100000;
    """

    df = pd.read_sql(query, conn)
    conn.close()

    st.success("✅ Sales data loaded successfully!")

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# -----------------------------
# Display Sample Data
# -----------------------------
st.subheader("📋 Sample Sales Data")
st.dataframe(df.head())

# -----------------------------
# KPI Section
# -----------------------------
st.subheader("📊 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Records",
        value=f"{len(df):,}"
    )

with col2:
    st.metric(
        label="Total Sales",
        value=f"{int(df['sales_quantity'].sum()):,}"
    )

with col3:
    st.metric(
        label="Average Sales",
        value=f"{df['sales_quantity'].mean():.2f}"
    )

st.divider()

# -----------------------------
# Sales Quantity Distribution
# -----------------------------
st.subheader("📦 Sales Quantity Distribution")

sales_distribution = (
    df["sales_quantity"]
    .value_counts()
    .sort_index()
)

st.bar_chart(sales_distribution)

# -----------------------------
# Daily Sales Trend
# -----------------------------
st.subheader("📈 Daily Sales Trend")

daily_sales = (
    df.groupby("date")["sales_quantity"]
      .sum()
      .reset_index()
)

st.line_chart(
    daily_sales,
    x="date",
    y="sales_quantity"
)

# -----------------------------
# Store-wise Sales
# -----------------------------
st.subheader("🏪 Store-wise Sales")

store_sales = (
    df.groupby("store_id")["sales_quantity"]
      .sum()
      .sort_values(ascending=False)
)

st.bar_chart(store_sales)

# -----------------------------
# Top 10 Selling Products
# -----------------------------
st.subheader("🔥 Top 10 Selling Products")

top_products = (
    df.groupby("item_id")["sales_quantity"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

st.bar_chart(top_products)

# -----------------------------
# Summary
# -----------------------------
st.divider()

st.info("""
### 📌 Dashboard Summary

- Displays sample sales records.
- Shows key sales KPIs.
- Visualizes sales quantity distribution.
- Displays daily sales trend.
- Compares sales across stores.
- Highlights the top 10 best-selling products.
""")