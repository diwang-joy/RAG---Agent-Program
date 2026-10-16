from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_community.chat_models import ChatTongyi

#创建所需的解析器
str_parser = StrOutputParser()

#创建模型
chat = ChatTongyi(model = "qwen3-max-2026-01-23")

#提示词模板
# prompt = PromptTemplate.from_template(
#     "你需要根据会话历史回应用户问题，对话历史: {chat_history}， 用户提问：{input}，请回答"
# )
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你需要根据会话历史回应用户问题，对话历史："),
        MessagesPlaceholder("chat_history"),
        ("human", "请回答如下问题：{input}")
    ]
)

base_chain = prompt | chat | str_parser

chat_history_store = {} #key就是session_id,value就是INmemoryChatMessageHistory类对象

def get_history(session_id):
    if session_id not in chat_history_store:
        chat_history_store[session_id] = InMemoryChatMessageHistory()
    return chat_history_store[session_id]

#创建一个新的链，对原有链增强功能：自动附加历史消息
conversation_chain = RunnableWithMessageHistory(
    base_chain,                        #被增强的原有链
    get_history,                       #通过会话ID获取INmemoryChatMessageHistory类对象
    input_messages_key="input",        #表示用户输入在模板中的占位符
    history_messages_key="chat_history"#表示历史消息在模板中的占位符
)

if __name__ == '__main__':
    #固定格式，添加langchain的配置，为当前程序配置所属的session_id
    session_config = {
        "configurable": {
            "session_id": "user_001"
        }
    }
    res = conversation_chain.invoke({"input": "小明有2只猫"}, session_config)
    print("第1次执行：", res)
    res = conversation_chain.invoke({"input": "小王有3条狗"}, session_config)
    print("第2次执行：", res)
    res = conversation_chain.invoke({"input": "小菊有8条狐狸"}, session_config)
    print("第3次执行：", res)
    res = conversation_chain.invoke({"input": "总共有几个宠物"}, session_config)
    print("第4次执行：", res)