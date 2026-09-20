import json
import hashlib
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.rag.store import vector_store
from backend import config

def sync_knowledge_base():
    """同步本地知识库"""
    data_path = config.DATA_DIR
    txt_files = list(data_path.glob("*.txt"))


    record_path = data_path/"file_records.json"

    if record_path.exists():
        file_records = json.loads(
            record_path.read_text(encoding="utf-8")
        )
    else:
        file_records = {}

    old_files = set(file_records.keys())

    current_files = set()

    for file_path in txt_files:
        current_files.add(file_path.name)

    new_documents = []
    # 创建分段器
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20,
        separators=["\n\n", "\n", "。", "，", "、", "！", "？", ""]
    )
    # 获取已有的文件源
    existing_sources = set(
        m["source"] for m in vector_store.get()["metadatas"]
        if m and "source" in m
    )
    # 遍历所有txt文件
    for file_path in txt_files:

        print("正在读取：", file_path.name)

        text = file_path.read_text(encoding="utf-8")

        # 计算文件的MD5值
        file_md5 = hashlib.md5(
            text.encode("utf-8")
        ).hexdigest()

        old_md5 = file_records.get(file_path.name)

        # file_records 可能滞后于向量库实际状态（同步中断、库被重建）
        # 只比对 MD5 会把缺失文件永久跳过，必须同时确认库里真有这个来源
        if old_md5 == file_md5 and file_path.name in existing_sources:
            print(file_path.name, "没有变化，跳过")
            continue

        print(file_path.name, "发生变化，需要更新")

        data = vector_store.get()

        for document_id, metadata in zip(
            data["ids"],
            data["metadatas"]
        ):
            if metadata and metadata["source"] == file_path.name:
                vector_store.delete(ids=[document_id])

        new_documents.extend(
            splitter.create_documents(
                [text],
                metadatas=[{"source": file_path.name}]
            )
        )

        file_records[file_path.name] = file_md5


    # 找出本地已经删除的文件
    deleted_files = old_files - current_files

    for deleted_file in deleted_files:
        print(deleted_file, "已经被删除，需要从知识库移除")

        data = vector_store.get()

        for document_id, metadata in zip(
                data["ids"],
                data["metadatas"]
        ):
            if metadata and metadata["source"] == deleted_file:
                vector_store.delete(ids=[document_id])

        del file_records[deleted_file]

    # 这里也在 for file_path 循环外
    if new_documents:
        vector_store.add_documents(new_documents)

    record_path.write_text(
        json.dumps(file_records, ensure_ascii=False, indent=4),
        encoding="utf-8"
    )