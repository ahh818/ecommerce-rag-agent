from backend.model import llm
from langchain.tools import tool
from backend.rag import RagService
from langchain.agents import create_agent
import time
from backend.chat_history import save_chat



rag_service = RagService()


@tool
def rag_summarize(query: str) -> str:
    """查询扫知识库，获取与用户问题相关的专业资料。"""
    return rag_service.rag_summarize(query)


@tool
def get_weather(city: str) -> str:
    """查询指定城市的天气"""
    return f"{city}今天晴天，25度"



system_prompt = """
你是智能客服。
只要用户询问任何在知识库中存在的相关问题，
必须调用查询知识库。
一个问题的回答如果同时涉及多个工具的信息，就在同一轮里同时调用多个工具，再综合两方面结果回答。
不要直接根据你自己的知识回答问题。
调用查询工具之后，
必须根据工具返回的知识库资料回答用户。
如果用户询问天气，可以调用 get_weather。
如果是普通聊天问题，不需要调用知识库。
"""


agent = create_agent(
    model=llm,
    tools=[rag_summarize, get_weather],
    system_prompt=system_prompt
)


messages = []

def execute_stream(messages):
    res = agent.stream(
        {
            "messages": messages
        },
        stream_mode="messages"
    )

    for chunk, metadata in res:

        if (
                metadata["langgraph_node"] == "model"
                and not chunk.tool_calls
                and chunk.content
        ):
          time.sleep(0.03)
          yield chunk.content


def chat(messages,query,chat_id):
    messages.append({
        "role": "user",
        "content": query
    })

    answer=""

    for text in execute_stream(messages):
        yield text
        answer += text

    messages.append({
        "role": "assistant",
        "content": answer
    })

    save_chat(messages, chat_id)