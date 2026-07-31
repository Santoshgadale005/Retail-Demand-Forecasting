# 🚀 Week 2 Summary — dbt Data Warehouse & Star Schema Architecture

## Goal
The focus of Week 2 was strictly **Data Engineering & Analytics Engineering**. We successfully migrated our basic Python-cleaned datasets into a highly normalized **Star Schema** Data Warehouse inside BigQuery using **dbt**.

## Key Achievements

### 1. The Staging Layer (Day 8 & 9)
- Established the `dbt_project/` repository.
- Modeled the raw tables into strictly typed `stg_` views.
- Built reusable Jinja macros (`clean_strings.sql`).

### 2. The Star Schema (Day 10 & 11)
- Built the `int_sales.sql` intermediate table.
- Scaffolded dimension tables (`dim_date`, `dim_product`, `dim_store`).
- Defined the core fact table `fct_sales` leveraging surrogate keys.

### 3. Analytics Marts & Data Quality (Day 12, 13, 14)
- Grouped the facts into Business Marts (`mart_daily_sales`, `mart_weekly`, etc.) to supply downstream ML models with instant, pre-calculated features.
- Enforced strict Data Quality tests through `schema.yml` ensuring primary key uniqueness, foreign key relationships, and valid numerical bounds (no negative sales).

**Status**: ✅ Week 2 Completed. We are fully prepared to train Machine Learning forecasting models on this data in Week 3!
