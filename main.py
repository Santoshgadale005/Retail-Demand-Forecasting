"""
Retail Demand Forecasting & Inventory Optimization
====================================================

Main application entry point for the retail demand forecasting
and inventory optimization platform.

This module provides:
    - Environment verification
    - BigQuery connection testing
    - Pipeline orchestration entry points
    - CLI interface for running individual components

Author: Santosh Gadale
Project: Retail Demand Forecasting & Inventory Optimization
Dataset: M5 Forecasting (Walmart Historical Sales Data)
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

# ===========================
# Configuration
# ===========================

# Load environment variables
load_dotenv()

# Project root directory
PROJECT_ROOT = Path(__file__).parent.resolve()

# Configure logging
logger.remove()  # Remove default handler
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
           "<level>{message}</level>",
    level=os.getenv("LOG_LEVEL", "INFO"),
)
logger.add(
    PROJECT_ROOT / "logs" / "app_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="30 days",
    level="DEBUG",
)


# ===========================
# Environment Verification
# ===========================

def verify_python_environment():
    """Verify Python version and installed packages."""
    logger.info("=" * 60)
    logger.info("🐍 Python Environment Verification")
    logger.info("=" * 60)

    # Python version
    python_version = sys.version
    logger.info(f"Python Version: {python_version}")

    if sys.version_info < (3, 10):
        logger.warning("⚠️  Python 3.10+ is recommended for this project")
    else:
        logger.success("✅ Python version is compatible")

    # Check critical packages
    critical_packages = {
        "pandas": "Data manipulation and analysis",
        "numpy": "Numerical computing",
        "matplotlib": "Static visualizations",
        "plotly": "Interactive visualizations",
        "sklearn": "Machine learning utilities",
        "lightgbm": "Gradient boosting forecasting",
        "prophet": "Time-series forecasting",
        "google.cloud.bigquery": "Google BigQuery client",
        "streamlit": "Dashboard framework",
        "sqlalchemy": "SQL toolkit",
        "dotenv": "Environment variable management",
        "loguru": "Logging framework",
        "tqdm": "Progress bars",
        "yaml": "YAML configuration parsing",
    }

    installed = []
    missing = []

    for package, description in critical_packages.items():
        try:
            __import__(package)
            installed.append(package)
            logger.info(f"  ✅ {package:<30} — {description}")
        except ImportError:
            missing.append(package)
            logger.warning(f"  ❌ {package:<30} — {description} [NOT INSTALLED]")

    logger.info("-" * 60)
    logger.info(f"Installed: {len(installed)}/{len(critical_packages)}")

    if missing:
        logger.warning(f"Missing packages: {', '.join(missing)}")
        logger.info("Run: pip install -r requirements.txt")
    else:
        logger.success("✅ All critical packages are installed!")

    return len(missing) == 0


def verify_environment_variables():
    """Verify required environment variables are set."""
    logger.info("=" * 60)
    logger.info("🔧 Environment Variables Verification")
    logger.info("=" * 60)

    required_vars = {
        "GCP_PROJECT_ID": "Google Cloud Project ID",
        "BQ_DATASET": "BigQuery Dataset Name",
        "BQ_LOCATION": "BigQuery Dataset Location",
    }

    optional_vars = {
        "GCP_CREDENTIALS_PATH": "GCP Service Account Key Path",
        "KAGGLE_USERNAME": "Kaggle API Username",
        "KAGGLE_KEY": "Kaggle API Key",
        "FORECAST_HORIZON": "Forecast Horizon (days)",
    }

    all_set = True

    logger.info("Required Variables:")
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value and value != f"your-{var.lower().replace('_', '-')}":
            logger.info(f"  ✅ {var:<30} = {value[:20]}...")
        else:
            logger.warning(f"  ❌ {var:<30} — {description} [NOT SET]")
            all_set = False

    logger.info("\nOptional Variables:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value and not value.startswith("your-") and not value.startswith("path/to"):
            logger.info(f"  ✅ {var:<30} = {value[:20]}...")
        else:
            logger.info(f"  ⏭️  {var:<30} — {description} [OPTIONAL]")

    return all_set


def verify_folder_structure():
    """Verify the project folder structure is intact."""
    logger.info("=" * 60)
    logger.info("📁 Folder Structure Verification")
    logger.info("=" * 60)

    required_dirs = [
        "data/raw",
        "data/processed",
        "data/external",
        "notebooks",
        "warehouse",
        "dbt_project",
        "forecasting/prophet",
        "forecasting/arima",
        "forecasting/lightgbm",
        "inventory",
        "streamlit",
        "reports",
        "dashboards",
        "deployment",
        "docker",
        "docs",
        "tests",
        "configs",
    ]

    all_exist = True
    for dir_path in required_dirs:
        full_path = PROJECT_ROOT / dir_path
        if full_path.exists():
            logger.info(f"  ✅ {dir_path}/")
        else:
            logger.warning(f"  ❌ {dir_path}/ [MISSING]")
            all_exist = False

    return all_exist


def verify_bigquery_connection():
    """Test the connection to Google BigQuery."""
    logger.info("=" * 60)
    logger.info("☁️  BigQuery Connection Verification")
    logger.info("=" * 60)

    try:
        from google.cloud import bigquery

        project_id = os.getenv("GCP_PROJECT_ID")
        credentials_path = os.getenv("GCP_CREDENTIALS_PATH")

        if credentials_path and os.path.exists(credentials_path):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        client = bigquery.Client(project=project_id)

        # Test connection by listing datasets
        dataset_name = os.getenv("BQ_DATASET", "retail_forecasting")
        dataset_ref = f"{project_id}.{dataset_name}"

        try:
            dataset = client.get_dataset(dataset_ref)
            logger.success(f"✅ BigQuery dataset '{dataset_name}' found!")
            logger.info(f"   Location: {dataset.location}")
            logger.info(f"   Created: {dataset.created}")
        except Exception:
            logger.warning(f"⚠️  Dataset '{dataset_name}' not found. "
                         "Create it in BigQuery Console or via CLI.")

        logger.success("✅ BigQuery connection successful!")
        return True

    except ImportError:
        logger.error("❌ google-cloud-bigquery not installed")
        return False
    except Exception as e:
        logger.error(f"❌ BigQuery connection failed: {e}")
        logger.info("💡 Ensure you've run: gcloud auth application-default login")
        return False


def run_verification():
    """Run all verification checks."""
    logger.info("🔍 Starting Environment Verification...")
    logger.info("=" * 60)

    results = {
        "Python Environment": verify_python_environment(),
        "Environment Variables": verify_environment_variables(),
        "Folder Structure": verify_folder_structure(),
        "BigQuery Connection": verify_bigquery_connection(),
    }

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("📊 Verification Summary")
    logger.info("=" * 60)

    for check, passed in results.items():
        status = "✅ PASSED" if passed else "⚠️  NEEDS ATTENTION"
        logger.info(f"  {check:<30} {status}")

    all_passed = all(results.values())
    if all_passed:
        logger.success("\n🎉 All checks passed! Environment is ready.")
    else:
        logger.warning("\n⚠️  Some checks need attention. "
                      "Review the output above and fix issues.")

    return all_passed


# ===========================
# CLI Interface
# ===========================

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Retail Demand Forecasting & Inventory Optimization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --verify          Verify development environment
  python main.py --etl             Run ETL pipeline
  python main.py --forecast        Run forecasting models
  python main.py --dashboard       Launch Streamlit dashboard
        """,
    )

    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify development environment setup",
    )
    parser.add_argument(
        "--etl",
        action="store_true",
        help="Run the ETL pipeline",
    )
    parser.add_argument(
        "--forecast",
        action="store_true",
        help="Run forecasting models",
    )
    parser.add_argument(
        "--dashboard",
        action="store_true",
        help="Launch the Streamlit dashboard",
    )

    return parser.parse_args()


def main():
    """Main application entry point."""
    args = parse_arguments()

    logger.info("🛒 Retail Demand Forecasting & Inventory Optimization")
    logger.info(f"   Project Root: {PROJECT_ROOT}")

    if args.verify:
        success = run_verification()
        sys.exit(0 if success else 1)

    elif args.etl:
        from etl.load_data import run_etl_pipeline
        success = run_etl_pipeline()
        sys.exit(0 if success else 1)

    elif args.forecast:
        logger.info("📈 Forecasting Models — Coming in Week 3")
        logger.info("   This will be implemented in upcoming days.")

    elif args.dashboard:
        logger.info("📊 Launching Streamlit Dashboard — Coming in Week 4")
        logger.info("   This will be implemented in upcoming days.")

    else:
        logger.info("Use --help to see available commands")
        logger.info("Use --verify to check environment setup")


if __name__ == "__main__":
    main()
