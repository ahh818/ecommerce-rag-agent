from backend.llm import llm
from langchain.agents import create_agent
import time
from backend.api.chat_history import save_chat
from backend.agent.tools import rag_summarize
from backend.agent.prompts import system_prompt




agent = create_agent(
    model=llm,
    tools=[rag_summarize],
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
          time.sleep(0.02)
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