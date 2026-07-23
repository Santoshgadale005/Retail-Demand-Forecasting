import os
import sys
from loguru import logger
import pandas as pd
from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPIError

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configs.settings import CONFIG, GCP_PROJECT_ID, GCP_CREDENTIALS_PATH

def save_local(calendar, sales, prices):
    """Save cleaned data to local processed dir as a fallback/checkpoint."""
    output_dir = CONFIG['paths']['processed_data']
    os.makedirs(output_dir, exist_ok=True)
    calendar.to_csv(os.path.join(output_dir, "calendar_clean.csv"), index=False)
    sales.to_csv(os.path.join(output_dir, "sales_clean.csv"), index=False)
    prices.to_csv(os.path.join(output_dir, "prices_clean.csv"), index=False)
    logger.info(f"Saved local cleaned data to {output_dir}")

def load_to_bigquery(df: pd.DataFrame, table_key: str):
    """Load dataframe to bigquery staging table."""
    dataset_id = CONFIG['bigquery']['dataset_id']
    table_name = CONFIG['bigquery']['staging_tables'].get(table_key)
    
    if not GCP_PROJECT_ID or GCP_PROJECT_ID == "your-gcp-project-id":
        logger.warning(f"GCP_PROJECT_ID not set or default. Skipping BigQuery upload for {table_key}.")
        return
        
    if GCP_CREDENTIALS_PATH and os.path.exists(GCP_CREDENTIALS_PATH):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GCP_CREDENTIALS_PATH
        
    try:
        client = bigquery.Client(project=GCP_PROJECT_ID)
        table_id = f"{GCP_PROJECT_ID}.{dataset_id}.{table_name}"
        
        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
        
        logger.info(f"Uploading {len(df)} rows to BigQuery table {table_id}...")
        job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()  # Wait for the job to complete
        
        logger.success(f"Successfully loaded {table_id}.")
    except Exception as e:
        logger.error(f"Failed to upload {table_key} to BigQuery: {e}")

def save_data(calendar, sales, prices):
    """Orchestrate saving local and loading to BQ."""
    save_local(calendar, sales, prices)
    load_to_bigquery(calendar, 'calendar')
    load_to_bigquery(sales, 'sales')
    load_to_bigquery(prices, 'prices')