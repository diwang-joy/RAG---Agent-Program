from openai import OpenAI

# 1.获取client对象，OpenAI类对象
client=OpenAI(
    base_url="https://ws-cqv7fu8oocwqlfk5.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

# 2.调用模型
response=client.chat.completions.create(
    model="qwen3-max-2026-01-23",
    messages=[
        {"role":"system", "content":"你是一个Python编程专家, 并且话很多"},
        {"role":"assistant", "content":"好的, 我是编程专家, 并且话不多, 你要问什么? "},
        {"role":"user", "content":"输出1-10的数字, 使用python代码"}
    ],
    stream=True  #开启流式输出功能
)

# 3.处理结果
# print(response.choices[0].message.content)
for chunk in response:
    print(
        chunk.choices[0].delta.content, 
        end=" ",                 #每一段之间以空格分隔
        flush=True               #立刻刷新缓冲区
    )