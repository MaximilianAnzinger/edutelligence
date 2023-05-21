"""Common place for environment variables with sensible defaults for local development."""
import os

PRODUCTION = os.environ.get("PRODUCTION", "0") == "1"
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///../data/data.sqlite")