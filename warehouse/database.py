"""
Warehouse Database Module
=========================

Provides a reusable database connection for the warehouse.
Uses the existing BigQueryConnection class, which automatically
falls back to a local SQLite database if BigQuery is unavailable.
"""

from etl.connection import BigQueryConnection


def get_connection():
    """
    Returns a database connection.

    Returns:
        BigQuery client or SQLite connection.
    """
    connection = BigQueryConnection()
    return connection.connect()