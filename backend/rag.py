from backend.model import llm
from langchain_core.prompts import ChatPromptTemplate
from backend.knowledge_base import sync_knowledge_base, vector_store

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

请使用参考资料回答，不要编造资料。
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

# if __name__ == "__main__":
#     """
#     测试RAG服务
#     """
#     rag_service = RagService()
#
#     query = "扫地机器人清扫完还有灰怎么办？"
#
#     answer = rag_service.rag_summarize(query)
#
#     print("========== 最终答案 ==========")
#     print(answer)
