import streamlit as st
from backend.agent.agent import chat
from datetime import datetime
from backend.chat_history import get_chat_list, get_chat_title, load_chat,delete_chat
from backend.rag.indexing import sync_knowledge_base
from pathlib import Path


#大标题
st.set_page_config(
    page_title="智能助手",
    page_icon="🤖"
)

if "messages" not in st.session_state:
    st.session_state["messages"]=[]

if "upload_key" not in st.session_state:
    st.session_state["upload_key"] = 0

if "chat_id" not in st.session_state:
    st.session_state["chat_id"] = datetime.now().strftime("%Y%m%d_%H%M%S")

# 标题
st.title("🤖 您的知心智能客服")
# 副标题
st.caption("基于 Agent + RAG 的智能客服")


# 显示消息
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 侧边栏
with st.sidebar:
    st.title("🤖 智慧通")

    st.caption("基于 Agent + RAG 的智能客服")

    st.divider()

    if st.button("➕ 新建对话"):
        st.session_state["messages"] = []
        st.session_state["chat_id"] = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.rerun()

    st.subheader("💬 历史对话")

    chat_list = get_chat_list()

    for chat_id in chat_list:

        chat_title = get_chat_title(chat_id)

        col1, col2 = st.columns([4, 1])

        with col1:
            if st.button(chat_title, key=f"chat_{chat_id}"):
                st.session_state["messages"] = load_chat(chat_id)
                st.session_state["chat_id"] = chat_id
                st.rerun()

        with col2:
            if st.button("🗑️", key=f"delete_{chat_id}"):
                delete_chat(chat_id)

                if st.session_state["chat_id"] == chat_id:
                    st.session_state["messages"] = []
                    st.session_state["chat_id"] = datetime.now().strftime("%Y%m%d_%H%M%S")

                st.rerun()



    st.divider()

    st.subheader("📚 知识库")

    data_path = Path("backend/data")

    txt_files = list(data_path.glob("*.txt"))

    if txt_files:
        for file_path in txt_files:
            st.write("📄", file_path.name)
    else:
        st.info("暂无知识库文件")

    st.divider()

    uploaded_file = st.file_uploader(
        "上传 TXT 知识库",
        type=["txt"],
        key=f"upload_{st.session_state['upload_key']}"
    )

    if uploaded_file is not None:
        st.write("① 开始保存文件")

        file_path = data_path / uploaded_file.name
        file_path.write_bytes(uploaded_file.getvalue())

        st.write("② 文件保存完成")

        sync_knowledge_base()

        st.write("③ 知识库同步完成")

        st.success("知识库添加成功！")

        st.session_state["upload_key"] += 1

        st.rerun()

    st.success("🟢 系统运行正常")


# 一些示例问题
st.write("💡 你可以这样问：")

col1, col2, col3 = st.columns(3)

with col1:
    question1 = st.button("扫地机器人怎么保养？")

with col2:
    question2 = st.button("为什么清扫后还有灰尘？")

with col3:
    question3 = st.button("尘盒多久清理一次？")

# 用户输入
prompt = st.chat_input("请输入你的问题")

if question1:
    prompt = "扫地机器人怎么保养？"

if question2:
    prompt = "为什么清扫后还有灰尘？"

if question3:
    prompt = "尘盒多久清理一次？"

if prompt:
    with st.chat_message("user"):
        st.write(prompt)

    response = chat(
        st.session_state["messages"],
        prompt,
        st.session_state["chat_id"]
    )

    with st.spinner("🤖 AI 正在思考..."):
         st.write_stream(response)

    st.rerun()