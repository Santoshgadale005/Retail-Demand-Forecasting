import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# -----------------------------------
# Page Configuration
# -----------------------------------
st.set_page_config(
    page_title="Inventory Dashboard",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Inventory Dashboard")

# -----------------------------------
# Load Data
# -----------------------------------
try:
    conn = sqlite3.connect("data/warehouse.db")

    query = """
    SELECT
        item_id,
        store_id,
        sales_quantity,
        sell_price
    FROM fact_sales
    """

    df = pd.read_sql(query, conn)
    conn.close()

    st.success("✅ Inventory data loaded successfully!")

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# -----------------------------------
# Sidebar Filter
# -----------------------------------
st.sidebar.header("🔍 Filters")

stores = sorted(df["store_id"].unique())

selected_store = st.sidebar.selectbox(
    "Select Store",
    ["All"] + list(stores)
)

if selected_store != "All":
    df = df[df["store_id"] == selected_store]

# -----------------------------------
# Inventory Summary
# -----------------------------------
inventory = (
    df.groupby("item_id")
      .agg(
          Total_Sales=("sales_quantity", "sum"),
          Average_Price=("sell_price", "mean")
      )
      .reset_index()
)

inventory["Inventory Value"] = (
    inventory["Total_Sales"] *
    inventory["Average_Price"]
)

inventory["Stock Status"] = inventory["Total_Sales"].apply(
    lambda x:
        "Low Stock" if x < 150 else
        "Medium Stock" if x < 500 else
        "High Stock"
)

# -----------------------------------
# KPI Cards
# -----------------------------------
low_stock = len(inventory[inventory["Stock Status"] == "Low Stock"])
medium_stock = len(inventory[inventory["Stock Status"] == "Medium Stock"])
high_stock = len(inventory[inventory["Stock Status"] == "High Stock"])

total_products = inventory["item_id"].nunique()
inventory_value = inventory["Inventory Value"].sum()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Products", total_products)

with col2:
    st.metric("Low Stock", low_stock)

with col3:
    st.metric("Medium Stock", medium_stock)

with col4:
    st.metric("High Stock", high_stock)

with col5:
    st.metric("Inventory Value", f"${inventory_value:,.2f}")

st.divider()

# -----------------------------------
# Inventory Distribution
# -----------------------------------
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
    title="Inventory Distribution",
    hole=0.45
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# Top Selling Products
# -----------------------------------
st.subheader("🏆 Top 10 Selling Products")

top_products = (
    inventory.sort_values(
        by="Total_Sales",
        ascending=False
    )
    .head(10)
)

fig = px.bar(
    top_products,
    x="item_id",
    y="Total_Sales",
    color="Total_Sales",
    title="Top 10 Products"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# Store-wise Sales
# -----------------------------------
st.subheader("🏪 Store-wise Sales")

store_sales = (
    df.groupby("store_id")["sales_quantity"]
      .sum()
      .reset_index()
)

fig = px.bar(
    store_sales,
    x="store_id",
    y="sales_quantity",
    color="sales_quantity",
    title="Store Sales Comparison"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# Inventory Statistics
# -----------------------------------
st.subheader("📈 Inventory Statistics")

st.dataframe(
    inventory.describe(),
    use_container_width=True
)

# -----------------------------------
# Inventory Details
# -----------------------------------
st.subheader("📋 Inventory Details")

st.dataframe(
    inventory,
    use_container_width=True
)

# -----------------------------------
# Low Stock Alert
# -----------------------------------
st.subheader("⚠️ Low Stock Items")

low_stock_items = inventory[
    inventory["Stock Status"] == "Low Stock"
]

if len(low_stock_items) > 0:
    st.warning(f"{len(low_stock_items)} products require restocking.")
    st.dataframe(low_stock_items, use_container_width=True)
else:
    st.success("🎉 No low-stock items found.")

# -----------------------------------
# Dashboard Summary
# -----------------------------------
st.divider()

st.info("""
### 📌 Dashboard Features

- ✅ Store Filter
- ✅ Inventory KPIs
- ✅ Inventory Value
- ✅ Stock Status Distribution
- ✅ Top 10 Products
- ✅ Store-wise Sales
- ✅ Inventory Statistics
- ✅ Low Stock Alerts
- ✅ Inventory Details Table
""")