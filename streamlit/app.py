import streamlit as st

st.set_page_config(
    page_title="Retail Demand Forecasting Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Retail Demand Forecasting Dashboard")

st.markdown("""
Welcome to the Retail Demand Forecasting Dashboard.

Use the sidebar to navigate between:

- 📈 Sales Overview
- 🔮 Demand Forecast
- 📦 Inventory Dashboard

This dashboard provides insights into sales performance, demand forecasting, and inventory management.
""")

st.success("Dashboard Loaded Successfully ✅")