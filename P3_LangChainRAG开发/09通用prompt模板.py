from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi

prompt_template = PromptTemplate.from_template(
    "我的邻居姓{lastname}, 刚生了{gender}孩,你帮我起个名字，简单回答"
)

# #调用.format方法注入信息即可
# prompt_text = prompt_template.format(lastname="王", gender="女")

# print(prompt_text)

model = Tongyi(model = "qwen-max") #这里放大语言模型，不放聊天模型

chain = prompt_template | model

res = chain.invoke(input={"lastname":"王", "gender":"女"})

print(res)