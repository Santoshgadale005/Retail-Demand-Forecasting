# 🧹 Day 5 Data Cleaning Report

## 1. Calendar Dataset (`stg_calendar`)
* **Standardization:** All column names converted to lowercase snake_case.
* **Dates:** Validated and standardized to standard pandas datetime format (`YYYY-MM-DD`).
* **Missing Values:**
  * Filled nulls in `event_name_1`, `event_type_1`, `event_name_2`, and `event_type_2` with "No Event" and "None" respectively.
* **Duplicates:** Dropped exact duplicates.
* **Result:** Clean staging table ready for BigQuery.

## 2. Sales Dataset (`stg_sales`)
* **Standardization:** Column names converted to lowercase snake_case.
* **Negative Values:** Validated sales records.
* **Duplicates:** Checked and dropped any row-level duplicates.
* **Note on Unpivoting:** The conversion from wide to long format (1,913 `d_` columns -> `date, sales_qty`) is deferred to BigQuery via `dbt` to prevent Python out-of-memory errors on massive datasets.

## 3. Pricing Dataset (`stg_prices`)
* **Standardization:** Column names converted to lowercase snake_case.
* **Negative Values:** Flagged and removed negative price entries to ensure validity.
* **Duplicates:** Dropped row-level duplicates.

## Next Steps
The data has been successfully staged and saved in `data/processed/`. The `google-cloud-bigquery` loader takes over to insert this into the `retail_forecasting` BigQuery dataset.
