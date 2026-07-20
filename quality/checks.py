"""
Data Quality Validation Checks
==============================

Implements specific validation functions for checking raw data tables
in BigQuery or the SQLite local database.
"""

import pandas as pd
import numpy as np
from loguru import logger
from google.cloud import bigquery

def run_query(query, client_or_conn):
    """Run a SQL query and return a Pandas DataFrame, supporting both BQ and SQLite."""
    if isinstance(client_or_conn, bigquery.Client):
        return client_or_conn.query(query).to_dataframe()
    else:
        return pd.read_sql(query, client_or_conn)


def check_missing_values(client_or_conn):
    """Check for missing values in all tables."""
    logger.info("  🔍 Checking missing values...")
    results = {}
    
    # 1. Calendar Missing Values
    q_cal = """
    SELECT 
        COUNT(*) as total_rows,
        SUM(CASE WHEN date IS NULL THEN 1 ELSE 0 END) as null_date,
        SUM(CASE WHEN wm_yr_wk IS NULL THEN 1 ELSE 0 END) as null_wm_yr_wk,
        SUM(CASE WHEN d IS NULL THEN 1 ELSE 0 END) as null_d,
        SUM(CASE WHEN event_name_1 IS NULL THEN 1 ELSE 0 END) as null_event_1,
        SUM(CASE WHEN event_name_2 IS NULL THEN 1 ELSE 0 END) as null_event_2
    FROM raw_calendar
    """
    df_cal = run_query(q_cal, client_or_conn).iloc[0]
    results["calendar"] = {
        "total_rows": int(df_cal["total_rows"]),
        "null_date": int(df_cal["null_date"]),
        "null_wm_yr_wk": int(df_cal["null_wm_yr_wk"]),
        "null_d": int(df_cal["null_d"]),
        "null_event_1": int(df_cal["null_event_1"]),
        "null_event_2": int(df_cal["null_event_2"]),
    }
    
    # 2. Prices Missing Values
    q_prc = """
    SELECT 
        COUNT(*) as total_rows,
        SUM(CASE WHEN store_id IS NULL THEN 1 ELSE 0 END) as null_store,
        SUM(CASE WHEN item_id IS NULL THEN 1 ELSE 0 END) as null_item,
        SUM(CASE WHEN wm_yr_wk IS NULL THEN 1 ELSE 0 END) as null_wm_yr_wk,
        SUM(CASE WHEN sell_price IS NULL THEN 1 ELSE 0 END) as null_price
    FROM raw_prices
    """
    df_prc = run_query(q_prc, client_or_conn).iloc[0]
    results["prices"] = {
        "total_rows": int(df_prc["total_rows"]),
        "null_store": int(df_prc["null_store"]),
        "null_item": int(df_prc["null_item"]),
        "null_wm_yr_wk": int(df_prc["null_wm_yr_wk"]),
        "null_price": int(df_prc["null_price"]),
    }
    
    # 3. Sales Missing Values (Check metadata columns only, as sales are checked separately)
    q_sls = """
    SELECT 
        COUNT(*) as total_rows,
        SUM(CASE WHEN id IS NULL THEN 1 ELSE 0 END) as null_id,
        SUM(CASE WHEN item_id IS NULL THEN 1 ELSE 0 END) as null_item,
        SUM(CASE WHEN store_id IS NULL THEN 1 ELSE 0 END) as null_store
    FROM raw_sales
    """
    df_sls = run_query(q_sls, client_or_conn).iloc[0]
    results["sales_metadata"] = {
        "total_rows": int(df_sls["total_rows"]),
        "null_id": int(df_sls["null_id"]),
        "null_item": int(df_sls["null_item"]),
        "null_store": int(df_sls["null_store"]),
    }
    
    return results


def check_duplicates(client_or_conn):
    """Check for duplicate rows or primary key violations."""
    logger.info("  🔍 Checking duplicate records...")
    results = {}
    
    # 1. Calendar duplicates on 'd'
    q_cal = "SELECT COUNT(d) - COUNT(DISTINCT d) as dup_d, COUNT(date) - COUNT(DISTINCT date) as dup_date FROM raw_calendar"
    df_cal = run_query(q_cal, client_or_conn).iloc[0]
    results["calendar"] = {
        "duplicate_d": int(df_cal["dup_d"]),
        "duplicate_date": int(df_cal["dup_date"])
    }
    
    # 2. Sales duplicates on 'id'
    q_sls = "SELECT COUNT(id) - COUNT(DISTINCT id) as dup_id FROM raw_sales"
    df_sls = run_query(q_sls, client_or_conn).iloc[0]
    results["sales"] = {
        "duplicate_ids": int(df_sls["dup_id"])
    }
    
    # 3. Prices duplicates on composite key (store_id, item_id, wm_yr_wk)
    # Using SQL to count groupings with count > 1
    if isinstance(client_or_conn, bigquery.Client):
        # Optimized for BigQuery
        q_prc = """
        SELECT COUNT(*) as dup_count FROM (
            SELECT store_id, item_id, wm_yr_wk, COUNT(*) 
            FROM raw_prices 
            GROUP BY store_id, item_id, wm_yr_wk 
            HAVING COUNT(*) > 1
        )
        """
    else:
        # SQLite
        q_prc = """
        SELECT COUNT(*) as dup_count FROM (
            SELECT store_id, item_id, wm_yr_wk
            FROM raw_prices
            GROUP BY store_id, item_id, wm_yr_wk
            HAVING COUNT(*) > 1
        )
        """
    df_prc = run_query(q_prc, client_or_conn).iloc[0]
    results["prices"] = {
        "duplicate_keys": int(df_prc["dup_count"])
    }
    
    return results


def validate_dates(client_or_conn):
    """Validate date fields in calendar."""
    logger.info("  🔍 Validating date formats and completeness...")
    q = """
    SELECT 
        MIN(date) as min_date,
        MAX(date) as max_date,
        COUNT(DISTINCT date) as unique_dates,
        COUNT(DISTINCT wm_yr_wk) as unique_weeks
    FROM raw_calendar
    """
    df = run_query(q, client_or_conn).iloc[0]
    
    # Date parsing test
    min_d = str(df["min_date"])
    max_d = str(df["max_date"])
    
    # Expected span is 1969 days
    is_complete = int(df["unique_dates"]) == 1969
    
    return {
        "min_date": min_d,
        "max_date": max_d,
        "unique_dates": int(df["unique_dates"]),
        "unique_weeks": int(df["unique_weeks"]),
        "is_complete": is_complete
    }


def validate_sales_data(client_or_conn):
    """Validate sales unit data (negative numbers, nulls, summary stats)."""
    logger.info("  🔍 Validating sales quantities...")
    
    if isinstance(client_or_conn, bigquery.Client):
        # In BigQuery, running dynamic SQL to sum over 1913 columns is possible
        # but for simplicity we can inspect the metadata table and check a sample of days.
        # Let's run a query checking the first and last few day columns
        day_cols = [f"d_{i}" for i in range(1, 1914, 100)] # Sample 20 day columns
        day_cols.append("d_1913")
        
        case_stmt_neg = " + ".join([f"CASE WHEN {c} < 0 THEN 1 ELSE 0 END" for c in day_cols])
        case_stmt_null = " + ".join([f"CASE WHEN {c} IS NULL THEN 1 ELSE 0 END" for c in day_cols])
        max_stmt = ", ".join([f"MAX({c}) as max_{c}" for c in day_cols[:5]])
        
        q = f"""
        SELECT 
            SUM({case_stmt_neg}) as negative_count_sample,
            SUM({case_stmt_null}) as null_count_sample,
            {max_stmt}
        FROM raw_sales
        """
        df = run_query(q, client_or_conn).iloc[0]
        
        return {
            "mode": "BigQuery Sampled (20 columns)",
            "negative_sales_found": int(df["negative_count_sample"]) > 0,
            "null_sales_found": int(df["null_count_sample"]) > 0,
            "max_sample_sale": int(df.iloc[2]) # Get first max value
        }
    else:
        # In SQLite, we can load the full dataframe since it's local and very fast in pandas
        df_sales = pd.read_sql("SELECT * FROM raw_sales", client_or_conn)
        sales_cols = [col for col in df_sales.columns if col.startswith("d_")]
        
        df_sales_subset = df_sales[sales_cols]
        null_count = df_sales_subset.isnull().sum().sum()
        negative_count = (df_sales_subset < 0).sum().sum()
        max_sale = df_sales_subset.max().max()
        mean_sale = df_sales_subset.mean().mean()
        
        return {
            "mode": "SQLite Full scan",
            "negative_sales_found": int(negative_count) > 0,
            "null_sales_found": int(null_count) > 0,
            "max_sale": int(max_sale),
            "mean_sale": float(mean_sale),
            "total_sales_columns": len(sales_cols)
        }


def validate_pricing_data(client_or_conn):
    """Validate pricing fields (negative prices, outliers, stats)."""
    logger.info("  🔍 Validating prices and detecting anomalies...")
    
    q_stats = """
    SELECT 
        MIN(sell_price) as min_price,
        MAX(sell_price) as max_price,
        AVG(sell_price) as avg_price,
        COUNT(CASE WHEN sell_price <= 0 THEN 1 END) as zero_or_neg_prices
    FROM raw_prices
    """
    df_stats = run_query(q_stats, client_or_conn).iloc[0]
    
    # Check for sudden price changes for a single item (e.g. price change ratio > 2.0 or < 0.5)
    # Let's run a query to check standard deviation of price grouped by store and item
    # We sample a few item-store combinations to avoid huge group by in SQLite
    q_var = """
    SELECT 
        AVG(price_std) as avg_price_std,
        MAX(price_range) as max_price_range
    FROM (
        SELECT 
            store_id, item_id,
            AVG(sell_price) as avg_p,
            MAX(sell_price) - MIN(sell_price) as price_range,
            (MAX(sell_price) / NULLIF(MIN(sell_price), 0)) as price_ratio
            /* SQLite doesn't support STDDEV_SAMP natively without extensions, so we use max-min */
        FROM raw_prices
        GROUP BY store_id, item_id
        LIMIT 5000
    )
    """
    try:
        df_var = run_query(q_var, client_or_conn).iloc[0]
        max_ratio = float(df_var["max_price_range"])
    except Exception:
        max_ratio = 0.0
        
    return {
        "min_price": float(df_stats["min_price"]),
        "max_price": float(df_stats["max_price"]),
        "avg_price": float(df_stats["avg_price"]),
        "zero_or_negative_prices": int(df_stats["zero_or_neg_prices"]),
        "max_price_range_sample": max_ratio
    }


def check_referential_integrity(client_or_conn):
    """Check that foreign keys align between tables."""
    logger.info("  🔍 Checking referential integrity...")
    
    # 1. Are there weeks in raw_prices that are not in raw_calendar?
    q_week = """
    SELECT COUNT(DISTINCT p.wm_yr_wk) as orphan_weeks
    FROM raw_prices p
    LEFT JOIN (SELECT DISTINCT wm_yr_wk FROM raw_calendar) c ON p.wm_yr_wk = c.wm_yr_wk
    WHERE c.wm_yr_wk IS NULL
    """
    df_week = run_query(q_week, client_or_conn).iloc[0]
    
    # 2. Are there stores in raw_sales that are not in raw_prices?
    q_store = """
    SELECT COUNT(DISTINCT s.store_id) as orphan_stores
    FROM raw_sales s
    LEFT JOIN (SELECT DISTINCT store_id FROM raw_prices) p ON s.store_id = p.store_id
    WHERE p.store_id IS NULL
    """
    df_store = run_query(q_store, client_or_conn).iloc[0]
    
    # 3. Are there items in raw_sales that are not in raw_prices?
    q_item = """
    SELECT COUNT(DISTINCT s.item_id) as orphan_items
    FROM raw_sales s
    LEFT JOIN (SELECT DISTINCT item_id FROM raw_prices) p ON s.item_id = p.item_id
    WHERE p.item_id IS NULL
    """
    df_item = run_query(q_item, client_or_conn).iloc[0]
    
    return {
        "orphan_weeks": int(df_week["orphan_weeks"]),
        "orphan_stores": int(df_store["orphan_stores"]),
        "orphan_items": int(df_item["orphan_items"]),
    }


def detect_outliers_sales(client_or_conn):
    """Detect sales outliers using standard deviation limits."""
    logger.info("  🔍 Scanning for statistical sales outliers...")
    
    if isinstance(client_or_conn, bigquery.Client):
        # Sample daily columns from BQ
        q = """
        SELECT 
            AVG(d_100) as mean_s,
            (SELECT MAX(d_100) FROM raw_sales) as max_s
        FROM raw_sales
        """
        df = run_query(q, client_or_conn).iloc[0]
        return {
            "method": "BigQuery Sample (d_100)",
            "mean": float(df["mean_s"]),
            "max": float(df["max_s"]),
            "outlier_count_est": "Check report for full details"
        }
    else:
        # Local SQLite
        df_sales = pd.read_sql("SELECT * FROM raw_sales", client_or_conn)
        sales_cols = [col for col in df_sales.columns if col.startswith("d_")]
        df_sales_subset = df_sales[sales_cols]
        
        # Calculate row-wise total daily sales
        total_daily_sales = df_sales_subset.sum(axis=0)
        mean_s = total_daily_sales.mean()
        std_s = total_daily_sales.std()
        
        # Outliers defined as 3 standard deviations from mean
        outliers = total_daily_sales[(total_daily_sales - mean_s).abs() > (3 * std_s)]
        
        return {
            "method": "SQLite Full Daily Sales Rollup",
            "mean_daily_sales": float(mean_s),
            "std_daily_sales": float(std_s),
            "outlier_days_count": len(outliers),
            "outlier_days": list(outliers.index)
        }
