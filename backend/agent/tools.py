from langchain.tools import tool
from backend.rag.pipeline import RagService


rag_service = RagService()


@tool
def rag_summarize(query: str) -> str:
    """查询知识库，获取与用户问题相关的专业资料。"""
    return rag_service.rag_summarize(query)
