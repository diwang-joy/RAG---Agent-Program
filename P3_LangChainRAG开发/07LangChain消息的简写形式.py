from langchain_community.chat_models.tongyi import ChatTongyi
# from langchain_core.messages import HumanMessage,SystemMessage,AIMessage

#初始化模型
chat = ChatTongyi(model = "qwen3-max-2026-01-23")

#准备消息List
messages = [
    # SystemMessage(content="你是一名来自边塞的诗人"),
    # HumanMessage(content="给我写一首唐诗"),
    # AIMessage(content="黑云压城城欲摧，甲光向日金鳞开。角声满天秋色里，塞上燕脂凝夜紫。半卷红旗临易水，霜重鼓寒声不起。报君黄金台上意，提携玉龙为君死！"),
    # HumanMessage(content="按照上面给你的内容生成一首相似的唐诗")
    ("system", "你是一名来自边塞的诗人"),
    ("human","给我写一首唐诗"),
    ("ai","黑云压城城欲摧，甲光向日金鳞开。角声满天秋色里，塞上燕脂凝夜紫。半卷红旗临易水，霜重鼓寒声不起。报君黄金台上意，提携玉龙为君死！"),
    ("human","按照上面给你的内容生成一首相似的唐诗")
]

#流式输出
res = chat.stream(input=messages)

for chunk in res:
    print(chunk.content, end="", flush=True)