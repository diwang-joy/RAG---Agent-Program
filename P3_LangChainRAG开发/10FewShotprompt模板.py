from langchain_core.prompts import PromptTemplate,FewShotPromptTemplate
from langchain_community.llms.tongyi import Tongyi

#示例的模板
example_template = PromptTemplate.from_template(
    "单词：{word}, 反义词：{antonym}"
)

#示例的动态数据注入，要求是list内部套字典
examples_data = [
    {"word": "大", "antonym": "小"},
    {"word": "上", "antonym": "下"}
]

few_shot_template = FewShotPromptTemplate(
    example_prompt=example_template, #示例数据的模板
    examples=examples_data,       #示例的数据（用来注入动态数据的），list内套字典  
    prefix="告知我单词的反义词，我提供如下的示例：",         #示例之前的提示词
    suffix="基于前面的示例告知我，{input_word}的反义词是？",         #示例之后的提示词
    input_variables=[]   #声明在前缀或后缀中所需要注入的变量名
)

# #调用.format方法注入信息即可
# prompt_text = prompt_template.format(lastname="王", gender="女")
prompt_text = few_shot_template.invoke(input={"input_word": "左"}).to_string()

print(prompt_text)

model = Tongyi(model = "qwen-max") #这里放大语言模型，不放聊天模型

print(model.invoke(input=prompt_text))

# chain = prompt_template | model

# res = chain.invoke(input={"lastname":"王", "gender":"女"})

# print(res)