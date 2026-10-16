from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个边塞诗人"), 
        # ("ai", "........"), 
        MessagesPlaceholder("history"), 
        ("human", "请再来一首唐诗")
    ]
)

histroy_data = [
    ("human", "你来写一首唐诗"),
    ("system", "床前明月光，疑是地上霜。举头望明月，低头思故乡"),
    ("human", "再来一首，要豪放的风格"),
    ("ai", "黑云压城城欲摧，甲光向日金鳞开。角声满天秋色里，塞上燕脂凝夜紫。半卷红旗临易水，霜重鼓寒声不起。报君黄金台上意，提携玉龙为君死！")
]

# prompt_values = chat_prompt_template.invoke({"history": histroy_data}).to_string()
# print(prompt_values)

model = ChatTongyi(model = "qwen3-max-2026-01-23")

#组成链，要求每一个组件都是Runnable接口的子类
chain = chat_prompt_template | model

#通过链去调用invoke或stream
res = chain.invoke({"history": histroy_data})
# res = model.invoke(prompt_values)
print(res.content, type(res))

#通过stream流式输出
for chunk in chain.stream({"history": histroy_data}):
    print(
        # chunk.choices[0].delta.content, 
        chunk.content,
        end=" ",                 #每一段之间以空格分隔
        flush=True               #立刻刷新缓冲区
    )