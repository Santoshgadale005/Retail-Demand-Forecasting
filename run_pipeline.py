from loguru import logger

# ETL
from etl.pipeline import run_pipeline as run_etl

def main():
    logger.info("=" * 60)
    logger.info("STARTING RETAIL ANALYTICS PIPELINE")
    logger.info("=" * 60)

    # Step 1: ETL
    logger.info("Running ETL Pipeline...")
    run_etl()

    logger.success("Pipeline completed successfully!")

if __name__ == "__main__":
    main()