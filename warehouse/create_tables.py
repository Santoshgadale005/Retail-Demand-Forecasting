"""
Create Warehouse Tables
=======================

Reads the schema.sql file and creates all warehouse tables.
"""

from pathlib import Path
import sqlite3
from configs.config import DATA_DIR


def create_tables():
    """Create warehouse tables in the local SQLite database."""

    # Database location
    db_path = DATA_DIR / "warehouse.db"

    # Connect to SQLite
    conn = sqlite3.connect(db_path)

    # Read SQL schema
    schema_path = Path(__file__).parent / "schema.sql"

    with open(schema_path, "r", encoding="utf-8") as file:
        sql_script = file.read()

    # Execute SQL
    conn.executescript(sql_script)

    conn.commit()
    conn.close()

    print("✅ Warehouse tables created successfully.")


if __name__ == "__main__":
    create_tables()