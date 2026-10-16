from langchain_core.output_parsers import StrOutputParser,JsonOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate

#创建所需的解析器
str_parser = StrOutputParser()
json_parser = JsonOutputParser()

#创建模型
chat = ChatTongyi(model = "qwen3-max-2026-01-23")

#第一个提示词模板
first_prompt = PromptTemplate.from_template(
    "我的邻居姓{lastname}, 刚生了{gender}孩,你帮我起个名字，并封装为JSON格式返回给我，要求key是name，value就是你起的名字，请严格遵守格式要求。"
)

#第二个提示词模板
second_prompt =  PromptTemplate.from_template(
    "请解析{name}的含义"
)

#构建链
chain = first_prompt | chat | json_parser | second_prompt | chat | str_parser

# res = chain.invoke(input={"lastname":"王", "gender":"女"})
# print(res)

res = chain.stream(input={"lastname":"王", "gender":"女"})
for chunk in res:
    print(chunk, end="", flush=True)
