from pathlib import Path
from datetime import datetime
import os
from dotenv import load_dotenv
from manim import *  # Import Manim's color constants
from pydantic import BaseModel

# Load environment variables from .env file
# This will look for .env in the current working directory and parent directories
env_path = Path(__file__).parent.parent.parent / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    # Fallback to src/.env for backward compatibility
    src_env_path = Path(__file__).parent.parent / '.env'
    if src_env_path.exists():
        load_dotenv(dotenv_path=src_env_path)

# Global Constants
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "o3-mini")
MANIM_QUALITY = "-ql"  # Low quality for faster rendering
EXECUTION_TIMEOUT = 180  # seconds
MAX_ATTEMPTS = 5


# Directory Configuration
BASE_DIR = Path(__file__).parent.parent.parent  # Points to /backend
PACKAGE_DIR = Path(__file__).parent.parent      # Points to /backend/askleap
GENERATED_DIR = BASE_DIR / "generated"
LOGS_DIR = GENERATED_DIR / "logs"
ASSETS_DIR = PACKAGE_DIR / "assets"             # Updated to point to /backend/askleap/assets
TEMPLATES_DIR = PACKAGE_DIR / "templates"       # Also update this to be consistent

# Ensure directories exist
GENERATED_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Run timestamp
RUN_TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
