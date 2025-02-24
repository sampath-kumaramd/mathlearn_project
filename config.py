import os
from dotenv import load_dotenv
import sys

try:
    load_dotenv(override=True)
except UnicodeDecodeError:
    print("Error: .env file has incorrect encoding. Please ensure it's saved as UTF-8")
    sys.exit(1)

# Database configuration with fallback values
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://PostgreSQL 17:1234@localhost:5432/mathlearn")

# Path configuration
MODEL_PATH = os.getenv("MODEL_PATH", "./models")
DATA_PATH = os.getenv("DATA_PATH", "./data")

# Application settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LANGUAGE = os.getenv("LANGUAGE", "si")
TTS_ENGINE = os.getenv("TTS_ENGINE", "gtts")
SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24))

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")