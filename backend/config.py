import os
from dotenv import load_dotenv
load_dotenv()

# Streamlit Cloud 部署时没有 .env 文件，配置在 Secrets 里（存于 st.secrets）。
# 这里把 st.secrets 灌进环境变量，让下面的 os.getenv 也能读到。
# 本地开发时 st.secrets 不存在，except 会静默跳过，仍然走 .env。
try:
    import streamlit as st
    for _k, _v in st.secrets.items():
        os.environ.setdefault(_k, str(_v))
except Exception:
    pass

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



