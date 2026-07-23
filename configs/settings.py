import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

def load_config(config_path="configs/config.yaml"):
    """Loads configuration from a YAML file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

# Load config globally for easy access
CONFIG = load_config()

# Read from .env if present
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_CREDENTIALS_PATH = os.getenv("GCP_CREDENTIALS_PATH")
