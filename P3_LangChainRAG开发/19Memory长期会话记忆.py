import os, json
from typing import Sequence
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
#message_to_dict: 单个消息对象（BaseMessage类实例）-> 字典
#messages_from_dict: [字典，字典...] -> [消息，消息...]
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_models import ChatTongyi

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, storage_path):
        self.session_id = session_id          #会话id
        self.storage_path = storage_path      #不同会话id的存储文件，所在的文件夹路径
        #完整的文件路径
        self.file_path = os.path.join(self.storage_path, self.session_id)

        #确保文件夹是存在的
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)      #已有的消息列表
        all_messages.extend(messages)           #新的和已有的融合成一个list

        #将数据同步写入到本地文件中
        #类对象写入文件 -> 一堆二进制
        #为了方便，可以将BaseMessage消息转为字典（借助json模块以json字符串写入文件）
        # new_messages = []
        # for message in all_messages:
        #     data = message_to_dict(message)
        #     new_messages.append(data)
        new_messages = [message_to_dict(message) for message in all_messages]
        #将数据写入文件
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f)

    @property
    def messages(self) -> list[BaseMessage]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []
        
    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)

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

# chat_history_store = {} #key就是session_id,value就是INmemoryChatMessageHistory类对象

def get_history(session_id):
    return FileChatMessageHistory(session_id, "./chat_history")

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
    # res = conversation_chain.invoke({"input": "小明有2只猫"}, session_config)
    # print("第1次执行：", res)
    # res = conversation_chain.invoke({"input": "小王有3条狗"}, session_config)
    # print("第2次执行：", res)
    # res = conversation_chain.invoke({"input": "小菊有8条狐狸"}, session_config)
    # print("第3次执行：", res)
    res = conversation_chain.invoke({"input": "总共有几个宠物"}, session_config)
    print("第4次执行：", res)