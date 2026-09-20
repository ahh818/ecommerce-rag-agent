from langchain_openai import ChatOpenAI
from backend import config


def create_llm():
    llm = ChatOpenAI(
        model=config.DEEPSEEK_MODEL,
        api_key=config.DEEPSEEK_API_KEY,
        temperature=config.TEMPERATURE,
        base_url=config.DEEPSEEK_BASE_URL,
    )
    return llm

llm = create_llm()

