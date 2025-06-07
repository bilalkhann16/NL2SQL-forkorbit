import os
from dotenv import load_dotenv
from loguru import logger
import sys

load_dotenv()


class Config:
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")
    LLM_MODEL = os.getenv("LLM_MODEL", "gemini-1.5-flash")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))  # Max retries for query validation


# Configure logging
logger.remove()
logger.add(
    "logs/nl2sql.log",
    rotation="10 MB",
    retention="7 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)
logger.add(
    sys.stdout, level="INFO", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)
