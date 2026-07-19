# 📋 Day 2 Summary — M5 Dataset Exploration & Data Warehouse Design

**Project**: Retail Demand Forecasting & Inventory Optimization  
**Date**: Day 2  
**Status**: ✅ Completed

---

## 🎯 Today's Objectives

| # | Task | Status | Details |
|---|------|--------|---------|
| 1 | Download the M5 Forecasting Dataset | ✅ | Retrieved Zenodo zip archive, extracted CSVs to `data/raw/` |
| 2 | Understand and Profile CSV structures | ✅ | Analyzed rows, columns, data types, and file sizes |
| 3 | Create Data Dictionary | ✅ | Documented schemas in `docs/data_dictionary.md` |
| 4 | Analyze Hierarchical Structure | ✅ | Mapped levels: Item → Department → Category → Store → State |
| 5 | Design BigQuery Warehouse Schema | ✅ | Outlined Raw, Staging, and Analytics (Star Schema) layers |
| 6 | Plan Partitioning & Clustering | ✅ | Optimized query paths on date partitions and store/item clusters |
| 7 | Identify Table Joins & ERD | ✅ | Mapped relationships between sales, calendar, and price tables |

---

## 📊 Dataset Profile Summary

Our profiling scripts analyzed the raw M5 dataset files and verified the following metadata:

*   **`sales_train_validation.csv`**:
    *   *Shape*: 30,490 rows x 1,919 columns (448.2 MB in memory)
    *   *Columns*: Metadata keys (`id`, `item_id`, `dept_id`, `cat_id`, `store_id`, `state_id`) + 1,913 daily sales series (`d_1` to `d_1913`)
*   **`calendar.csv`**:
    *   *Shape*: 1,969 rows x 14 columns (0.26 MB)
    *   *Columns*: `date` (DATE), `wm_yr_wk` (INT64), `weekday` (STR), `wday` (INT64), events (STR), and state SNAP indicators (INT64)
*   **`sell_prices.csv`**:
    *   *Shape*: 6,841,121 rows x 4 columns (318.1 MB)
    *   *Columns*: `store_id` (STR), `item_id` (STR), `wm_yr_wk` (INT64), `sell_price` (FLOAT64)

---

## 🏛️ Data Warehouse Architecture

To store this data efficiently, we designed a **three-tier BigQuery warehouse architecture**:

1.  **Raw Layer**: Direct ingestion of raw files into `raw_calendar`, `raw_sales`, and `raw_prices`.
2.  **Staging Layer**: Transformation models using dbt to unpivot the wide `raw_sales` data into long format (58 million rows of `date`, `item_id`, `store_id`, `sales_quantity`).
3.  **Analytics Layer (Star Schema)**:
    *   `fact_sales`: Partitioned daily by `date`, clustered by `(store_id, item_id)`.
    *   `dim_product`: Holds item, department, and category metadata.
    *   `dim_store`: Holds store and state mappings.
    *   `dim_date`: Calendar date parameters, event flags, and SNAP indicators.

---

## 💡 Key Design Decisions & Strategies

*   **SQLite Fallback Development Mode**: Due to GCP credential requirements, we implemented a dual connection mechanism in python. If BigQuery authentication fails, the pipeline gracefully falls back to local SQLite (`data/warehouse.db`), allowing full development and testing on local workstations.
*   **Partitioning**: We selected daily partition on `date` for `fact_sales` to reduce scan size.
*   **Clustering**: We chose clustering on `(store_id, item_id)` for both `fact_sales` and `raw_prices` to maximize join performance.

---

## 🔄 Git Activity (Prepared)

Suggested commit message (no commits were made yet as requested):
```
Day 2: Analyzed M5 dataset and designed initial data warehouse schema
```

---

## 📅 Next Steps — Day 3 Preview

Tomorrow we will implement the ETL pipeline scripts under `etl/` and load the raw CSV files into our target tables (`raw_sales`, `raw_calendar`, `raw_prices`).
