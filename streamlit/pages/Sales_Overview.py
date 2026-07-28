import streamlit as st
import pandas as pd
import sqlite3

# -----------------------------------
# Page Configuration
# -----------------------------------
st.set_page_config(
    page_title="Sales Overview",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Sales Overview Dashboard")

# -----------------------------------
# Load Data
# -----------------------------------
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

# -----------------------------------
# Sidebar Filters
# -----------------------------------
st.sidebar.header("🔍 Filters")

store_list = sorted(df["store_id"].unique())

selected_store = st.sidebar.selectbox(
    "Select Store",
    ["All"] + list(store_list)
)

if selected_store != "All":
    df = df[df["store_id"] == selected_store]

# -----------------------------------
# Sample Data
# -----------------------------------
st.subheader("📋 Sample Sales Data")
st.dataframe(df.head(10), use_container_width=True)

# -----------------------------------
# KPI Section
# -----------------------------------
st.subheader("📊 Key Performance Indicators")

total_records = len(df)
total_sales = int(df["sales_quantity"].sum())
average_sales = round(df["sales_quantity"].mean(), 2)
total_revenue = (df["sales_quantity"] * df["sell_price"]).sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Records",
        f"{total_records:,}"
    )

with col2:
    st.metric(
        "Total Sales",
        f"{total_sales:,}"
    )

with col3:
    st.metric(
        "Average Sales",
        f"{average_sales}"
    )

with col4:
    st.metric(
        "Revenue",
        f"${total_revenue:,.2f}"
    )

st.divider()

# -----------------------------------
# Sales Quantity Distribution
# -----------------------------------
st.subheader("📦 Sales Quantity Distribution")

sales_distribution = (
    df["sales_quantity"]
    .value_counts()
    .sort_index()
)

st.bar_chart(sales_distribution)

# -----------------------------------
# Daily Sales Trend
# -----------------------------------
st.subheader("📈 Daily Sales Trend")

daily_sales = (
    df.groupby("date")["sales_quantity"]
      .sum()
      .reset_index()
)

st.line_chart(
    daily_sales,
    x="date",
    y="sales_quantity",
    use_container_width=True
)

# -----------------------------------
# Store-wise Sales
# -----------------------------------
st.subheader("🏪 Store-wise Sales")

store_sales = (
    df.groupby("store_id")["sales_quantity"]
      .sum()
      .sort_values(ascending=False)
)

st.bar_chart(store_sales)

# -----------------------------------
# Revenue by Store
# -----------------------------------
st.subheader("💰 Revenue by Store")

store_revenue = (
    df.groupby("store_id")
      .apply(lambda x: (x["sales_quantity"] * x["sell_price"]).sum())
      .sort_values(ascending=False)
)

st.bar_chart(store_revenue)

# -----------------------------------
# Top 10 Selling Products
# -----------------------------------
st.subheader("🔥 Top 10 Selling Products")

top_products = (
    df.groupby("item_id")["sales_quantity"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

st.bar_chart(top_products)

# -----------------------------------
# Sales Statistics
# -----------------------------------
st.subheader("📋 Sales Statistics")

st.dataframe(
    df["sales_quantity"].describe().to_frame(name="Statistics"),
    use_container_width=True
)

# -----------------------------------
# Dashboard Summary
# -----------------------------------
st.divider()

st.info("""
### 📌 Dashboard Summary

✅ Displays sample sales records

✅ Interactive store filter

✅ Key Performance Indicators (KPIs)

✅ Sales quantity distribution

✅ Daily sales trend

✅ Store-wise sales comparison

✅ Revenue by store

✅ Top 10 best-selling products

✅ Sales statistics
""")