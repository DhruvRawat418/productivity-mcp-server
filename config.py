# config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(ENV_PATH)

# Use pathlib (NOT os.path)
GMAIL_API_KEY = os.getenv("GMAIL_API_KEY")
CALENDAR_API_KEY = os.getenv("GOOGLE_CALENDAR_API_KEY")
TASK_DB_PATH = Path(os.getenv("TASK_DB_PATH", "./tasks.json"))

# Validation
if not GMAIL_API_KEY:
    raise ValueError("GMAIL_API_KEY not found in .env")
