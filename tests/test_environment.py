"""
Test Environment Setup
======================

Tests to verify the development environment is correctly configured.
Run with: pytest tests/test_environment.py -v
"""

import os
import sys
from pathlib import Path

import pytest


# Project root (one level up from tests/)
PROJECT_ROOT = Path(__file__).parent.parent.resolve()


class TestPythonEnvironment:
    """Verify Python environment configuration."""

    def test_python_version(self):
        """Python version should be 3.10 or higher."""
        assert sys.version_info >= (3, 10), (
            f"Python 3.10+ required, got {sys.version}"
        )

    def test_virtual_environment_active(self):
        """A virtual environment should be active."""
        # Check for venv or conda
        in_venv = (
            hasattr(sys, "real_prefix")
            or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)
            or os.getenv("CONDA_DEFAULT_ENV") is not None
        )
        # Not strictly required — just a warning
        if not in_venv:
            pytest.skip("Virtual environment not detected (optional)")


class TestCriticalPackages:
    """Verify critical packages are installed."""

    @pytest.mark.parametrize("package", [
        "pandas",
        "numpy",
        "matplotlib",
        "plotly",
        "sklearn",
        "lightgbm",
        "google.cloud.bigquery",
        "streamlit",
        "sqlalchemy",
        "dotenv",
        "loguru",
        "tqdm",
        "yaml",
    ])
    def test_package_installed(self, package):
        """Critical package should be importable."""
        __import__(package)


class TestFolderStructure:
    """Verify project folder structure."""

    @pytest.mark.parametrize("directory", [
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
    ])
    def test_directory_exists(self, directory):
        """Required directory should exist."""
        path = PROJECT_ROOT / directory
        assert path.exists(), f"Directory missing: {directory}/"
        assert path.is_dir(), f"Not a directory: {directory}/"


class TestConfigurationFiles:
    """Verify configuration files exist."""

    @pytest.mark.parametrize("filename", [
        "README.md",
        "requirements.txt",
        ".gitignore",
        ".env",
        "main.py",
        "LICENSE",
        "configs/config.py",
    ])
    def test_file_exists(self, filename):
        """Required configuration file should exist."""
        path = PROJECT_ROOT / filename
        assert path.exists(), f"File missing: {filename}"
        assert path.stat().st_size > 0, f"File is empty: {filename}"


class TestEnvironmentVariables:
    """Verify environment variables are defined (not necessarily valid)."""

    def test_env_file_exists(self):
        """The .env file should exist."""
        env_path = PROJECT_ROOT / ".env"
        assert env_path.exists(), ".env file missing"

    def test_env_file_has_gcp_vars(self):
        """The .env file should contain GCP configuration."""
        env_path = PROJECT_ROOT / ".env"
        content = env_path.read_text()
        assert "GCP_PROJECT_ID" in content
        assert "BQ_DATASET" in content
        assert "BQ_LOCATION" in content
