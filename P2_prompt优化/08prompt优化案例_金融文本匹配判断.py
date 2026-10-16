from openai import OpenAI
import json

# 1.获取client对象，OpenAI类对象
client=OpenAI(
    base_url="https://ws-cqv7fu8oocwqlfk5.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

examples_data = {
    #示例数据
    "是":[
        ("中科曙光","曙光信息产业股份有限公司"),
        ("贵州茅台一季度净利润同比增长 15%，超出市场普遍预期。","茅台一季度盈利表现亮眼，净利增幅达两位数，超越分析师预测。")
    ],
    "不是":[
        ("中科曙光","中科信息"),
        ("该公司 2025 年第一季度实现营收 25.86 亿元。","该公司 2025 年第一季度实现营收 258.6 亿元。")
    ]
}

#提问数据
questions = [
    ("多家券商给予中科曙光“买入”评级，认为 AI 算力需求将推动其估值持续修复。","某私募基金指出，中科曙光当前市盈率已处于历史高位，短期内存在回调压力，建议投资者逢高减持。"),
    ("预计 2026 年上半年归属于上市公司股东的净利润为 4.2 亿元至 4.5 亿元，同比增长约 18%~22%。","该公司上半年盈利预计实现超两成增长，净利区间落在 4.2 亿至 4.5 亿元。"),
    ("2026年7月15日，某大型公募基金增持了宁德时代（300750）约 120 万股。","2026年7月16日，宁德时代披露公告，称某机构投资者通过大宗交易减持了 120 万股。")
]

messages = [
    {"role":"system", "content": f"你帮我完成文本匹配，我给你句子，被[]包围，你判断它们是否匹配，回答是或者不是"}
]

for key, value in examples_data.items():
    for t in value:
        messages.append({"role":"user", "content": f"句子1：[{t[0]}]，句子2：[{t[1]}]"})
        messages.append({"role":"assistant", "content": key})

# for x in messages:
#     print(x)

#2.向模型提问(调用模型)
for q in questions:
    response=client.chat.completions.create(
        model="qwen3-max-2026-01-23",
        messages=messages+[{"role":"user", "content":f"句子1：[{q[0]}]，句子2：[{q[1]}]"}]
        # f 告诉 Python 解释器：这个字符串里的 {q} 不是普通文本，而是一个占位符。运行时，{q} 会被替换为变量 q 当前存储的实际内容。
    )

#3.处理结果
    print(response.choices[0].message.content)