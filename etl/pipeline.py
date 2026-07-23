import os
import sys
import time
from loguru import logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configs.settings import CONFIG
from etl.extract import load_data as extract_data
from etl.clean import clean_calendar, clean_sales, clean_prices
from etl.load import save_data

def setup_logging():
    log_dir = CONFIG['paths']['log_dir']
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "etl.log")
    logger.add(log_file, rotation="10 MB", level="INFO")
    logger.info("="*50)
    logger.info("Initializing Automated ETL Pipeline")
    logger.info("="*50)

def run_pipeline():
    setup_logging()
    start_time = time.time()
    
    try:
        # Extract
        logger.info("Phase 1: Extracting Raw Data")
        calendar, sales, prices = extract_data()
        
        # Clean
        logger.info("Phase 2: Transforming & Cleaning Data")
        calendar = clean_calendar(calendar)
        sales = clean_sales(sales)
        prices = clean_prices(prices)
        
        # Load
        logger.info("Phase 3: Loading Data to Staging")
        save_data(calendar, sales, prices)
        
        elapsed = time.time() - start_time
        logger.success(f"ETL Pipeline Completed Successfully in {elapsed:.2f} seconds!")
        
    except Exception as e:
        logger.exception(f"ETL Pipeline Failed due to a critical error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()