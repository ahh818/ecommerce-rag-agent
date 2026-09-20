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
请根据下面的参考资料回答用户问题。
参考资料：
{context}
用户问题：
{query}
请先判断：参考资料中是否包含回答该问题所需的信息？
- 如果包含：基于参考资料回答，不要编造。
- 如果不包含：明确告诉用户"知识库中没有相关内容"，
  不要尝试用你自己的知识回答。
""")

    def rag_summarize(self,query:str) ->str:
        """
        RAG总结
        :param query:
        :return:
        """
        # 1. 根据问题检索相关文档
        results = self.retriever.invoke(query)
        # 2. 把检索到的文档拼接成一个字符串
        context = "\n".join([result.page_content for result in results])
        # 3. 把context和query拼接成一个字符串
        prompt = self.prompt_template.format_prompt(context=context, query=query)
        # 4. 调用大模型
        answer = llm.invoke(prompt)

        # 5. 返回答案文本
        return answer.content