from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi

parser = StrOutputParser()

chat = ChatTongyi(model = "qwen3-max-2026-01-23")

prompt_template = PromptTemplate.from_template(
    "我的邻居姓{lastname}, 刚生了{gender}孩,你帮我起个名字，简单回答"
)

chain = prompt_template | chat | parser | chat

res = chain.invoke(input={"lastname":"王", "gender":"女"})

print(res.content)