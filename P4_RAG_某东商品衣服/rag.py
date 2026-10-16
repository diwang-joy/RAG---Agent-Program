from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatTongyi
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
import file_history_store
from langchain_core.runnables import RunnableWithMessageHistory, RunnableLambda

def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt

class RagService(object):

    def __init__(self):

        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings()
        )

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "以我提供的已知参考资料为主，"
                 "简洁和专业的回答用户问题。参考资料: {context}。"),
                ("system", "并且我提供用户的对话历史记录，如下："),
                MessagesPlaceholder("history"),
                ("user", "请回答用户提问：{input}")
            ]
        )

        self.chat_model = ChatTongyi(model = config.chat_model)

        self.chain = self.__get_chain()

    #获取最终的执行链
    def __get_chain(self):
        retriever = self.vector_service.get_retriever()

        def format_func(docs: list[Document]):
            if not docs:
                return "无相关参考资料"
            formatted_str = ""
            # formatted_str = "["
            for doc in docs:
                formatted_str += f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n"
            # formatted_str += "]"
            return formatted_str
        
        def format_for_retriever(value: dict) -> str:
            return value["input"]
        
        def format_for_prompt_template(value):
            #{input, context, history}
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["context"] = value["context"]
            new_value["history"] = value["input"]["history"]
            return new_value
    
        chain = (
            {
                "input": RunnablePassthrough(), 
                "context": RunnableLambda(format_for_retriever) | retriever | format_func
            } | RunnableLambda(format_for_prompt_template) | self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
        )

        #创建一个新的链，对原有链增强功能：自动附加历史消息
        conversation_chain = RunnableWithMessageHistory(
            chain,                        #被增强的原有链
            file_history_store.get_history,                       #通过会话ID获取INmemoryChatMessageHistory类对象
            input_messages_key="input",        #表示用户输入在模板中的占位符
            history_messages_key="history"#表示历史消息在模板中的占位符
        )

        return conversation_chain
    
if __name__ == "__main__":
    #session_id配置
    session_config = {
        "configurable": {
            "session_id": "user_001",
        }
    }
    
    res = RagService().chain.invoke({"input": "羊毛衫应该怎么保养？"}, session_config)
    print(res)