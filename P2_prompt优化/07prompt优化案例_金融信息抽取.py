from openai import OpenAI
import json

# 1.获取client对象，OpenAI类对象
client=OpenAI(
    base_url="https://ws-cqv7fu8oocwqlfk5.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

schema = ['日期', '股票名称', '开盘价', '收盘价', '成交量']
examples_data = [   #示例数据
    {
        "contents":"2026年7月30日,当日上证指数低开，开盘报3812.11点，盘中最高触及3839.34点，最低下探至3767.50点，最终收于3804.69点，下跌23.78点，跌幅0.62%。沪深两市合计成交额约2.34万亿元。",
        "answers":{
            "日期":"2026年7月30日",
            "股票名称":"当日上证指数",
            "开盘价":"3812.11点",
            "收盘价":"3804.69点",
            "成交量":"2.34万亿元"
        }
    },
    {
        "contents":"2026年7月30日,贵州茅台当日表现强劲，开盘报1323.00元，较昨日收盘价1321.00元小幅高开，盘中最高触及1362.00元，最低1322.00元，最终收于1361.76元，大涨40.76元，涨幅3.09%，成交额达97.12亿元。",
        "answers":{
            "日期":"2026年7月30日",
            "股票名称":"贵州茅台",
            "开盘价":"1323.00元",
            "收盘价":"1361.76元",
            "成交量":"97.12亿元"
        }
    }        
]

#提问数据
questions = [
    "2026年7月30日,宁德时代当日开盘报390.00元，较昨日收盘价396.84元低开，盘中最高冲至403.80元，最低389.80元，最终收于401.88元，上涨5.04元，涨幅1.27%，成交额达181.03亿元。",
    "2026年7月30日,中科曙光当日大幅下跌，开盘报85.49元，盘中最高仅触及86.65元，最低下探至80.55元，最终收于81.00元，下跌5.64元，跌幅高达6.51%，成交额55.58亿元。"
]

messages = [
    {"role":"system", "content": f"你帮我完成信息抽取，我给你句子，你抽取{schema}信息，按JSON字符串输出，如果某些信息不存在，用'原文未提及'输出"}
    # {"role":"user", "content":"XXX发布了2XXX年第X季度业绩快报......"},
    # {"role":"assistant", "content":"新闻报道"},
    # {"role":"user", "content":"从资产端看，报告期末总资产为XXX亿元......"},
    # {"role":"assistant", "content":"财务报告"},
    # {"role":"user", "content":"XXX公司董事会在公告中表示......"},
    # {"role":"assistant", "content":"公司公告"},
    # {"role":"user", "content":"XXX扣非净利润同比增长XX%......"},
    # {"role":"assistant", "content":"分析师报告"},
    # {"role":"user", "content":"要提问的问题"}
]

for example in examples_data:
    messages.append({"role":"user", "content":example["contents"]})
    messages.append({"role":"assistant", "content":json.dumps(example["answers"], ensure_ascii=False)})

# for x in messages:
#     print(x)

#2.向模型提问(调用模型)
for q in questions:
    response=client.chat.completions.create(
        model="qwen3-max-2026-01-23",
        messages=messages+[{"role":"user", "content":f"按照示例，抽取这个句子的信息：{q}"}]
        # f 告诉 Python 解释器：这个字符串里的 {q} 不是普通文本，而是一个占位符。运行时，{q} 会被替换为变量 q 当前存储的实际内容。
    )

#3.处理结果
    print(response.choices[0].message.content)