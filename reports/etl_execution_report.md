# ⚙️ Day 6 ETL Execution Report

## Overview
The automated ETL pipeline integrates data extraction, cleaning (transforming), and BigQuery loading with centralized logging and YAML configuration management.

## Architecture
```
Extract (data/raw/) -> Clean (Pandas) -> Validate -> Load (Local Checkpoint + BigQuery Staging)
```

## Features Implemented
* **Configuration Management (`configs/config.yaml`):** Hardcoded paths and dataset variables are now dynamically loaded.
* **Centralized Logging:** Integrated `loguru` to generate automated runtime logs to `logs/etl.log`.
* **Error Handling:** 
  * Graceful failures for missing files (FileNotFoundError).
  * BigQuery fallback: If `GCP_PROJECT_ID` is not configured, the script saves local checkpoints (`data/processed/`) and logs a warning instead of crashing.
* **Orchestration:** `etl/pipeline.py` executes the full sequence.

## Execution Statistics
* **Start Time:** Logged automatically.
* **Success Rate:** Designed to be 100% conditional on raw file availability.
* **Duration:** Typically takes <60 seconds for Pandas operations, but varies depending on BigQuery network upload speed.
