"""
ETL Data Ingestion Script
==========================

Reads raw M5 Forecasting CSV files, validates their schema, and loads them
into Google BigQuery (or a local SQLite database fallback).
"""

import os
import sys
import time
from pathlib import Path
import pandas as pd
from loguru import logger
from google.cloud import bigquery

# Add project root to path to allow configs imports
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.append(str(PROJECT_ROOT))

from configs.config import (
    RAW_DATA_DIR,
    BQ_DATASET,
    BQ_LOCATION,
    M5_FILES,
    BQ_TABLES
)
from etl.connection import BigQueryConnection

def verify_raw_files():
    """Verify that all required raw M5 dataset CSV files exist."""
    logger.info("🔍 Verifying raw CSV files existence...")
    missing_files = []
    
    for key, filename in M5_FILES.items():
        file_path = RAW_DATA_DIR / filename
        if not file_path.exists():
            # Check sales_train_validation specifically
            logger.error(f"❌ Missing file: {filename} at {file_path}")
            missing_files.append(filename)
        else:
            size_mb = file_path.stat().st_size / (1024 * 1024)
            logger.info(f"  ✅ Found {filename} ({size_mb:.2f} MB)")
            
    if missing_files:
        raise FileNotFoundError(f"Missing raw files: {', '.join(missing_files)}")
    
    logger.success("✅ All required raw files verified successfully!")


def load_calendar_data(connection_obj, client_or_conn):
    """Load raw calendar data."""
    file_path = RAW_DATA_DIR / M5_FILES["calendar"]
    logger.info(f"📅 Ingesting calendar data from {file_path.name}...")
    
    # Read calendar CSV
    df = pd.read_csv(file_path)
    logger.info(f"   Loaded dataframe shape: {df.shape}")
    
    # Validation: check dates
    if df['date'].isnull().any():
        logger.warning("⚠️ Warning: Found null values in calendar date column!")
        
    start_time = time.time()
    
    if isinstance(client_or_conn, bigquery.Client):
        # BigQuery Load
        table_ref = BQ_TABLES["raw_calendar"]
        logger.info(f"   Loading to BigQuery table: {table_ref}...")
        
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True
        )
        
        with open(file_path, "rb") as source_file:
            job = client_or_conn.load_table_from_file(
                source_file, table_ref, job_config=job_config
            )
            job.result()  # Wait for job to complete
            
        table = client_or_conn.get_table(table_ref)
        elapsed = time.time() - start_time
        logger.success(f"   Successfully loaded {table.num_rows} rows to BQ in {elapsed:.2f}s")
        return table.num_rows
    else:
        # SQLite Load
        table_name = "raw_calendar"
        logger.info(f"   Loading to SQLite table: {table_name}...")
        df.to_sql(table_name, client_or_conn, if_exists="replace", index=False)
        
        # Verify count
        cursor = client_or_conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        elapsed = time.time() - start_time
        logger.success(f"   Successfully loaded {row_count} rows to SQLite in {elapsed:.2f}s")
        return row_count


def load_prices_data(connection_obj, client_or_conn):
    """Load raw sell prices data."""
    file_path = RAW_DATA_DIR / M5_FILES["sell_prices"]
    logger.info(f"💰 Ingesting selling prices data from {file_path.name}...")
    
    start_time = time.time()
    
    if isinstance(client_or_conn, bigquery.Client):
        # BigQuery Load
        table_ref = BQ_TABLES["raw_prices"]
        logger.info(f"   Loading to BigQuery table: {table_ref} (Direct File Load)...")
        
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True
        )
        
        with open(file_path, "rb") as source_file:
            job = client_or_conn.load_table_from_file(
                source_file, table_ref, job_config=job_config
            )
            job.result()  # Wait for job to complete
            
        table = client_or_conn.get_table(table_ref)
        elapsed = time.time() - start_time
        logger.success(f"   Successfully loaded {table.num_rows} rows to BQ in {elapsed:.2f}s")
        return table.num_rows
    else:
        # SQLite Load (chunked load because sell_prices is 6.8 million rows)
        table_name = "raw_prices"
        logger.info(f"   Loading to SQLite table: {table_name} in chunks...")
        
        # Clear/Create table by writing first chunk with replace
        chunksize = 100000
        first_chunk = True
        total_rows = 0
        
        for chunk in pd.read_csv(file_path, chunksize=chunksize):
            if first_chunk:
                chunk.to_sql(table_name, client_or_conn, if_exists="replace", index=False)
                first_chunk = False
            else:
                chunk.to_sql(table_name, client_or_conn, if_exists="append", index=False)
            total_rows += len(chunk)
            
        elapsed = time.time() - start_time
        logger.success(f"   Successfully loaded {total_rows} rows to SQLite in {elapsed:.2f}s")
        return total_rows


def load_sales_data(connection_obj, client_or_conn):
    """Load raw sales training data."""
    file_path = RAW_DATA_DIR / M5_FILES["sales_train_validation"]
    logger.info(f"📦 Ingesting sales train validation data from {file_path.name}...")
    
    start_time = time.time()
    
    if isinstance(client_or_conn, bigquery.Client):
        # BigQuery Load
        table_ref = BQ_TABLES["raw_sales"]
        logger.info(f"   Loading to BigQuery table: {table_ref} (Direct File Load)...")
        
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True
        )
        
        with open(file_path, "rb") as source_file:
            job = client_or_conn.load_table_from_file(
                source_file, table_ref, job_config=job_config
            )
            job.result()  # Wait for job to complete
            
        table = client_or_conn.get_table(table_ref)
        elapsed = time.time() - start_time
        logger.success(f"   Successfully loaded {table.num_rows} rows to BQ in {elapsed:.2f}s")
        return table.num_rows
    else:
        # SQLite Load
        table_name = "raw_sales"
        logger.info(f"   Loading to SQLite table: {table_name}...")
        df = pd.read_csv(file_path)
        df.to_sql(table_name, client_or_conn, if_exists="replace", index=False)
        
        # Verify count
        cursor = client_or_conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        elapsed = time.time() - start_time
        logger.success(f"   Successfully loaded {row_count} rows to SQLite in {elapsed:.2f}s")
        return row_count


def create_bq_dataset_if_not_exists(client):
    """Create BigQuery dataset if it doesn't already exist."""
    dataset_id = f"{client.project}.{BQ_DATASET}"
    logger.info(f"🛠️ Creating BigQuery dataset '{dataset_id}' if it does not exist...")
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = BQ_LOCATION
    try:
        client.create_dataset(dataset, exists_ok=True)
        logger.success(f"✅ BigQuery dataset '{BQ_DATASET}' is ready.")
    except Exception as e:
        logger.error(f"❌ Failed to create BigQuery dataset: {e}")
        raise e


def run_etl_pipeline():
    """Orchestrate the entire ETL pipeline."""
    logger.info("=" * 60)
    logger.info("🔄 STARTING ETL PIPELINE")
    logger.info("=" * 60)
    
    start_time = time.time()
    
    # 1. Verify input files
    try:
        verify_raw_files()
    except Exception as e:
        logger.critical(f"❌ ETL Initialization failed: {e}")
        return False
        
    # 2. Establish connection
    db_conn = BigQueryConnection()
    client_or_conn = db_conn.connect()
    
    # 3. Create dataset if BigQuery
    if isinstance(client_or_conn, bigquery.Client):
        try:
            create_bq_dataset_if_not_exists(client_or_conn)
        except Exception as e:
            logger.critical(f"❌ Dataset preparation failed: {e}")
            db_conn.close()
            return False
            
    # 4. Ingest tables
    summary = {}
    success = True
    try:
        # Load Calendar
        summary["raw_calendar"] = load_calendar_data(db_conn, client_or_conn)
        
        # Load Sales
        summary["raw_sales"] = load_sales_data(db_conn, client_or_conn)
        
        # Load Prices
        summary["raw_prices"] = load_prices_data(db_conn, client_or_conn)
        
    except Exception as e:
        logger.error(f"❌ ETL Ingestion failed: {e}")
        success = False
    finally:
        db_conn.close()
        
    # 5. Output Summary
    elapsed_total = time.time() - start_time
    logger.info("=" * 60)
    logger.info("📊 ETL PIPELINE EXECUTION SUMMARY")
    logger.info("=" * 60)
    
    if success:
        logger.success(f"Status: SUCCESS (Completed in {elapsed_total:.2f}s)")
        for table, rows in summary.items():
            logger.info(f"  - {table:<15}: {rows:,} rows successfully loaded")
    else:
        logger.error(f"Status: FAILED (Completed in {elapsed_total:.2f}s)")
        
    return success


if __name__ == "__main__":
    run_etl_pipeline()
