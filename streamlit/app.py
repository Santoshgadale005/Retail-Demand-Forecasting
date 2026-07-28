import streamlit as st

st.set_page_config(
    page_title="Retail Demand Forecasting Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Retail Demand Forecasting Dashboard")

st.markdown("### Welcome to the Retail Analytics System")

st.write(
    """
This dashboard provides insights into retail sales,
inventory management, and demand forecasting.
Use the navigation menu on the left to explore the dashboards.
"""
)

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Sales",
        value="125,678 Units",
        delta="+8.5%"
    )

with col2:
    st.metric(
        label="Revenue",
        value="$458,230",
        delta="+12.3%"
    )

with col3:
    st.metric(
        label="Forecast Sales",
        value="12,673 Units",
        delta="+4.8%"
    )

with col4:
    st.metric(
        label="Stores",
        value="10",
        delta="0"
    )

st.divider()

st.subheader("📌 Dashboard Modules")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
### 📈 Sales Overview

- Daily Sales
- Monthly Sales
- Revenue Trends
- Top Products
""")

with col2:
    st.success("""
### 🔮 Demand Forecast

- Sales Prediction
- Forecast Charts
- Trend Analysis
- Future Demand
""")

with col3:
    st.warning("""
### 📦 Inventory Dashboard

- Stock Levels
- Inventory Status
- Low Stock Alerts
- Product Availability
""")

st.divider()

st.success("✅ Dashboard Loaded Successfully")