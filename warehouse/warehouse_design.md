# Retail Demand Forecasting Data Warehouse

## Fact Table

### fact_sales

- date
- item_id
- store_id
- sales_quantity
- sell_price

---

## Dimension Tables

### dim_calendar

- date
- weekday
- month
- year
- event_name
- event_type

### dim_item

- item_id
- department
- category

### dim_store

- store_id
- state

---

## Star Schema

dim_calendar
↓

fact_sales

↑

dim_item

↑

dim_store