from pathlib import Path
import json


CHAT_DIR = Path(__file__).resolve().parent / "data" / "chats"

# 保存聊天记录
def save_chat(messages, chat_id):
    chat_path = CHAT_DIR / f"{chat_id}.json"

    chat_path.write_text(
        json.dumps(messages, ensure_ascii=False, indent=4),
        encoding="utf-8"
    )

# 加载聊天记录
def load_chat(chat_id):
    chat_path = CHAT_DIR / f"{chat_id}.json"

    if not chat_path.exists():
        return []

    return json.loads(
        chat_path.read_text(encoding="utf-8")
    )

# 获取聊天记录列表
def get_chat_list():
    chat_files = CHAT_DIR.glob("*.json")

    chat_list = []

    for chat_file in chat_files:
        chat_id = chat_file.stem
        chat_list.append(chat_id)

    return chat_list

# 获取聊天记录标题
def get_chat_title(chat_id):
    messages = load_chat(chat_id)

    for message in messages:
        if message["role"] == "user":
            return message["content"]


    return "新对话"


# 删除聊天记录
def delete_chat(chat_id):

    chat_path = CHAT_DIR / f"{chat_id}.json"

    if chat_path.exists():
        chat_path.unlink()
