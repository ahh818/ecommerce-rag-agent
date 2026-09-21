from langchain_core.prompts import ChatPromptTemplate
from backend.rag.indexing import sync_knowledge_base
from backend.rag.store import vector_store
from backend.llm import llm


class RagService :
    def __init__(self):
        """
        初始化RAG服务
        """
        #启动时同步本地知识库
        sync_knowledge_base()
        #创建检索器
        self.retriever = vector_store.as_retriever(
            search_kwargs={"k": 4}
        )
        self.prompt_template = ChatPromptTemplate.from_template("""
参考资料：
{context}
用户问题：
{query}
请先判断：参考资料中是否包含回答该问题所需的信息？
- 如果包含：基于参考资料回答，不要编造。
- 如果不包含：明确告诉用户"知识库中没有相关内容"，
  不要尝试用你自己的知识回答。
  判断过程不要出现在回答里，只输出最终回答。
""")

    def rag_summarize(self,query:str) ->str:
        """
        RAG总结
        :param query:
        :return:
        """
        # 1. 检索
        results = self.retriever.invoke(query)

        # 2. 收集来源文件（去重，保持顺序）
        sources = list(dict.fromkeys(
            r.metadata.get("source")
            for r in results
            if r.metadata.get("source")
        ))

        # 3. 拼 context（原有逻辑）
        context = "\n".join([r.page_content for r in results])

        # 4. 调模型（原有逻辑）
        prompt = self.prompt_template.format_prompt(context=context, query=query)
        answer = llm.invoke(prompt).content

        # 5. 附上来源引用
        if sources:
            answer += "\n\n📚 来源：" + "、".join(sources)

        return answer