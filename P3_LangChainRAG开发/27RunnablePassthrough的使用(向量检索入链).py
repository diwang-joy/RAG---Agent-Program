from langchain_chroma import Chroma
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


#初始化模型
chat = ChatTongyi(model = "qwen3-max-2026-01-23")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "以我提供的参考资料为主，简洁和专业的回答用户问题，参考资料:{context}"),
        ("user", "用户提问: {input}")
    ]
)

def print_prompt(prompt):
    print(prompt.to_string())
    print("="*20)
    return prompt

vector_store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings()
)

#准备向量库的数据
vector_store.add_texts(["黑云压城城欲摧", "甲光向日金鳞开", "角声满天秋色里", "塞上燕脂凝夜紫", "半卷红旗临易水", "霜重鼓寒声不起", "报君黄金台上意", "提携玉龙为君死"])

input_text = "生成一首风格相似的唐诗"

#langchain中向量存储对象，有一个方法：as_retriever. 可以返回一个runnable接口的子类实例对象
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

def format_func(docs):
    if not docs:
        return "无参考资料"
    formatted_str = "["
    for doc in docs:
        formatted_str += doc.page_content
    formatted_str += "]"
    return formatted_str

chain = (
    {"input": RunnablePassthrough(), "context": retriever | format_func} | prompt | print_prompt | chat | StrOutputParser()
)

res = chain.invoke(input_text)
print(res)