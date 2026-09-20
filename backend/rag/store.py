from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma
from backend import config

embed_model = DashScopeEmbeddings(
    model="text-embedding-v4",
    dashscope_api_key=config.DASHSCOPE_API_KEY
)


vector_store = Chroma(
    collection_name=config.COLLECTION_NAME,
    embedding_function=embed_model,
    persist_directory=config.PERSIST_DIR
)
