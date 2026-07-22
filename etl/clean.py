import pandas as pd
from loguru import logger

def clean_calendar(calendar):
    """Standardize and clean calendar data."""
    logger.info("Starting calendar cleaning...")
    df = calendar.copy()
    
    # Standardize column names
    df.columns = [c.strip().lower() for c in df.columns]
    
    # Standardize dates
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        if df['date'].isnull().any():
            logger.warning(f"Found {df['date'].isnull().sum()} invalid dates in calendar.")
    
    # Handle missing event names
    for col in ['event_name_1', 'event_type_1', 'event_name_2', 'event_type_2']:
        if col in df.columns:
            df[col] = df[col].fillna("No Event")
            
    # Drop duplicates
    initial_len = len(df)
    df = df.drop_duplicates()
    if len(df) < initial_len:
        logger.info(f"Dropped {initial_len - len(df)} duplicate rows in calendar.")
        
    logger.info("Calendar cleaning completed.")
    return df

def clean_sales(sales):
    """Clean sales dataset."""
    logger.info("Starting sales cleaning...")
    df = sales.copy()
    
    # Standardize columns
    df.columns = [c.strip().lower() for c in df.columns]
    
    # Drop duplicates
    initial_len = len(df)
    df = df.drop_duplicates()
    if len(df) < initial_len:
        logger.info(f"Dropped {initial_len - len(df)} duplicate rows in sales.")
        
    # NOTE: Massive unpivoting of `d_` columns is deferred to dbt staging model to prevent OOM
    # For day 5, we ensure basic integrity and save it for staging load.
    
    logger.info("Sales cleaning completed.")
    return df

def clean_prices(prices):
    """Clean prices dataset."""
    logger.info("Starting prices cleaning...")
    df = prices.copy()
    
    # Standardize columns
    df.columns = [c.strip().lower() for c in df.columns]
    
    # Validate negative prices
    if 'sell_price' in df.columns:
        invalid_prices = df[df['sell_price'] < 0]
        if not invalid_prices.empty:
            logger.warning(f"Found {len(invalid_prices)} negative price records. Removing them.")
            df = df[df['sell_price'] >= 0]
            
    # Drop duplicates
    initial_len = len(df)
    df = df.drop_duplicates()
    if len(df) < initial_len:
        logger.info(f"Dropped {initial_len - len(df)} duplicate rows in prices.")
        
    logger.info("Prices cleaning completed.")
    return df
