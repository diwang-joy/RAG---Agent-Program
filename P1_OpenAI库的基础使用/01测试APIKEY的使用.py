from openai import OpenAI
import os

client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    # api_key=os.getenv("DASHSCOPE_API_KEY"),
    # api_key="sk-ws-H.EHYIEPM.Iubo.MEQCIGE1HifwmjrUWeEQpjXPD2w70HEevD4QKS-6233A_kNaAiBSZTYNLEVgzs99s5t_yV1cSbfqqMKFAPKnobIzBViujw",
    base_url="https://ws-cqv7fu8oocwqlfk5.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    # base_url="http://localhost:11434/v1", #ollama
)

messages = [{"role": "user", "content": "你是谁"}]
completion = client.chat.completions.create(
    model="qwen3-max-2026-01-23",  # 您可以按需更换为其它深度思考模型
    # model="qwen3.6", #ollama
    messages=messages,
    extra_body={"enable_thinking": True},
    stream=True
)
is_answering = False  # 是否进入回复阶段
print("\n" + "=" * 20 + "思考过程" + "=" * 20)
for chunk in completion:
    if not chunk.choices:
        continue
    delta = chunk.choices[0].delta
    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
        if not is_answering:
            print(delta.reasoning_content, end="", flush=True)
    if hasattr(delta, "content") and delta.content:
        if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20)
            is_answering = True
        print(delta.content, end="", flush=True)