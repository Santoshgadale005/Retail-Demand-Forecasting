import os
import pandas as pd
from loguru import logger
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configs.settings import CONFIG

def load_data():
    """Load all raw datasets."""
    raw_path = CONFIG['paths']['raw_data']
    cal_file = os.path.join(raw_path, CONFIG['files']['calendar'])
    sales_file = os.path.join(raw_path, CONFIG['files']['sales'])
    prices_file = os.path.join(raw_path, CONFIG['files']['prices'])
    
    try:
        logger.info(f"Extracting calendar from {cal_file}")
        calendar = pd.read_csv(cal_file)
        logger.info(f"Extracting sales from {sales_file}")
        sales = pd.read_csv(sales_file)
        logger.info(f"Extracting prices from {prices_file}")
        prices = pd.read_csv(prices_file)
        logger.info("Extraction completed successfully.")
        return calendar, sales, prices
    except FileNotFoundError as e:
        logger.error(f"Failed to find file: {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred during extraction: {e}")
        raise

if __name__ == "__main__":
    calendar, sales, prices = load_data()
    print("Calendar Shape:", calendar.shape)