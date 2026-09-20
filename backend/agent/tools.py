from langchain.tools import tool
from backend.rag.pipeline import RagService



rag_service = RagService()


@tool
def rag_summarize(query: str) -> str:
    """查询扫知识库，获取与用户问题相关的专业资料。"""
    return rag_service.rag_summarize(query)


@tool
def get_weather(city: str) -> str:
    """查询指定城市的天气"""
    return f"{city}今天晴天，25度"
