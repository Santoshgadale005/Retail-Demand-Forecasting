# 📋 Day 9 Summary — Build dbt Staging Models & Source Definitions

**Project**: Retail Demand Forecasting & Inventory Optimization  
**Date**: Day 9  
**Status**: ✅ Completed

---

## 🎯 Today's Objectives

| # | Task | Status | Details |
|---|------|--------|---------|
| 1 | Create Source YAML | ✅ | Created `dbt_project/models/staging/sources.yml` |
| 2 | Create Staging Models | ✅ | Created `stg_sales.sql`, `stg_calendar.sql`, `stg_prices.sql` |
| 3 | Rename Columns | ✅ | Applied snake_case standardizations in SQL |
| 4 | Cast Data Types | ✅ | Ensured integers and floats are strictly typed in BigQuery |
| 5 | Remove Unused Columns | ✅ | Filtered out irrelevant raw data artifacts |
| 6 | Create Common Macros | ✅ | Built `macros/clean_strings.sql` for string manipulation |
| 7 | Apply Materialization | ✅ | Defaulted staging models to `view` materialization |

---

## ⚙️ Summary of Staging Models

We constructed the first layer of our Data Warehouse (the Staging Layer).
* **Sources:** We formally defined our raw tables (`stg_calendar`, `stg_sales`, `stg_prices`) inside `sources.yml` to allow dbt to track lineage and perform freshness checks.
* **Macros:** We implemented a `clean_string` macro to standardize text fields (trimming whitespace and lowercasing) dynamically.
* **Staging SQL:** We casted identifiers to strings/ints where appropriate and explicitly defined the schemas. The massive wide sales unpivoting relies heavily on structural assumptions, which is appropriately documented.

---

## 📁 Key Files Reference

*   `dbt_project/models/staging/sources.yml`: Source data registry.
*   `dbt_project/models/staging/stg_calendar.sql`: Calendar staging logic.
*   `dbt_project/models/staging/stg_sales.sql`: Sales staging logic.
*   `dbt_project/models/staging/stg_prices.sql`: Price staging logic.
*   `dbt_project/macros/clean_strings.sql`: Reusable string standardizer.

---

## 🔄 Git Activity (Prepared)

Suggested commit message (no commits were made yet as requested):
```text
Day 9: Created dbt staging models for sales, calendar, and pricing data
```

---

## 📅 Next Steps — Day 10 Preview

Tomorrow we will join these staging models together in an Intermediate layer to generate business-ready metrics like holiday flags and joined weekly pricing.
