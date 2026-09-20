import os
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path

DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

TEMPERATURE = float(os.getenv("TEMPERATURE", "0.0"))

TAVILY_MAX_SEARCH_CALLS_PER_RUN = int(
    os.getenv("TAVILY_MAX_SEARCH_CALLS_PER_RUN", "1")
)

PERSIST_DIR = str(Path(__file__).resolve().parent/ "data" / "chroma_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")