from langchain_community.llms.tongyi import Tongyi

model = Tongyi(model = "qwen-max") #这里放大语言模型，不放聊天模型

res = model.invoke(input="你是谁呀能做什么")

print(res)