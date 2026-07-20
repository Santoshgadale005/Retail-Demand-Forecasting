"""
BigQuery Connection Module
==========================

Handles authentication and connection to Google BigQuery.
Supports local SQLite database fallback for local-only development and testing
when Google Cloud credentials are not configured.
"""

import os
import sqlite3
from google.cloud import bigquery
from google.oauth2 import service_account
from loguru import logger
from configs.config import GCP_PROJECT_ID, GCP_CREDENTIALS_PATH, DATA_DIR

class BigQueryConnection:
    """Manages connection to BigQuery with local database fallback capability."""
    
    def __init__(self):
        self.project_id = os.getenv("GCP_PROJECT_ID", GCP_PROJECT_ID)
        self.credentials_path = os.getenv("GCP_CREDENTIALS_PATH", GCP_CREDENTIALS_PATH)
        self.use_local_sqlite = os.getenv("USE_LOCAL_SQLITE", "False").lower() == "true"
        self._client = None
        self._sqlite_conn = None

    def connect(self):
        """Establish connection to BigQuery or fall back to local SQLite."""
        if self.use_local_sqlite:
            logger.info("🔌 USE_LOCAL_SQLITE is set to True. Using local database.")
            return self._connect_sqlite()
            
        # Try connecting to Google BigQuery
        try:
            if self.credentials_path and os.path.exists(self.credentials_path):
                logger.info(f"🔑 Connecting to BigQuery using service account key: {self.credentials_path}")
                credentials = service_account.Credentials.from_service_account_file(self.credentials_path)
                self._client = bigquery.Client(credentials=credentials, project=self.project_id)
            else:
                logger.info("☁️ Connecting to BigQuery using Application Default Credentials (ADC)")
                self._client = bigquery.Client(project=self.project_id)
                
            # Verify connection by retrieving project details
            self._client.get_project(self.project_id)
            logger.success("✅ Connected to Google BigQuery successfully!")
            return self._client
            
        except Exception as e:
            logger.warning(f"⚠️ Failed to connect to BigQuery: {e}")
            logger.info("🔄 Falling back to local SQLite database for development/testing.")
            return self._connect_sqlite()

    def _connect_sqlite(self):
        """Establish connection to a local SQLite database."""
        db_path = DATA_DIR / "warehouse.db"
        logger.info(f"📁 Local database path: {db_path}")
        try:
            self._sqlite_conn = sqlite3.connect(db_path)
            logger.success("✅ Connected to local SQLite database successfully!")
            return self._sqlite_conn
        except Exception as e:
            logger.critical(f"❌ Failed to connect to local SQLite: {e}")
            raise e

    def close(self):
        """Close connections."""
        if self._sqlite_conn:
            self._sqlite_conn.close()
            logger.info("🔒 Closed SQLite database connection.")
