import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Inventory Dashboard",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Inventory Dashboard")

# -----------------------------
# Load Data
# -----------------------------
try:
    conn = sqlite3.connect("data/warehouse.db")

    query = """
    SELECT item_id,
           store_id,
           sales_quantity
    FROM fact_sales
    """

    df = pd.read_sql(query, conn)
    conn.close()

    st.success("Inventory data loaded successfully!")

except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

# -----------------------------
# Inventory Summary
# -----------------------------
inventory = (
    df.groupby("item_id")["sales_quantity"]
      .sum()
      .reset_index()
)

inventory.rename(
    columns={"sales_quantity": "Total Sales"},
    inplace=True
)

# Create Stock Status
inventory["Stock Status"] = inventory["Total Sales"].apply(
    lambda x: "Low Stock" if x < 150 else
              "Medium Stock" if x < 500 else
              "High Stock"
)

# -----------------------------
# KPI Cards
# -----------------------------
low_stock = len(inventory[inventory["Stock Status"] == "Low Stock"])
medium_stock = len(inventory[inventory["Stock Status"] == "Medium Stock"])
high_stock = len(inventory[inventory["Stock Status"] == "High Stock"])

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Low Stock Items", low_stock)

with col2:
    st.metric("Medium Stock Items", medium_stock)

with col3:
    st.metric("High Stock Items", high_stock)

st.divider()

# -----------------------------
# Stock Status Chart
# -----------------------------
st.subheader("📊 Inventory Status Distribution")

status_counts = (
    inventory["Stock Status"]
    .value_counts()
    .reset_index()
)

status_counts.columns = ["Stock Status", "Count"]

fig = px.pie(
    status_counts,
    names="Stock Status",
    values="Count",
    hole=0.4,
    title="Inventory Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Top Selling Products
# -----------------------------
st.subheader("🏆 Top 10 Products")

top_products = (
    inventory.sort_values(
        by="Total Sales",
        ascending=False
    )
    .head(10)
)

fig2 = px.bar(
    top_products,
    x="item_id",
    y="Total Sales",
    title="Top Selling Products"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Inventory Table
# -----------------------------
st.subheader("📋 Inventory Details")

st.dataframe(inventory)

# -----------------------------
# Summary
# -----------------------------
st.info("""
### Dashboard Features

- Inventory KPIs
- Stock Status Distribution
- Top Selling Products
- Inventory Details Table
""")