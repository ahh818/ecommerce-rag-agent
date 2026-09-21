import os
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path

# 路径（以文件位置为锚，不随启动目录变化）
BACKEND_DIR = Path(__file__).resolve().parent   # backend 目录（数据都在这下面）
DATA_DIR = BACKEND_DIR / "data"                 # 数据根目录 ★ 唯一事实来源
PERSIST_DIR = str(DATA_DIR / "chroma_db")

# 环境变量
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

COLLECTION_NAME = os.getenv("COLLECTION_NAME")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.0"))
