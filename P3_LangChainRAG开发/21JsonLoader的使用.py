from langchain_community.document_loaders import JSONLoader

# loader = JSONLoader(
#     file_path = "./data/stu.json",
#     # jq_schema=".name",
#     # jq_schema=".other.addr"#抽取二级字典
#     jq_schema=".",
#     text_content=False       #告知jsonloader所抽取的内容不是字符串
#     # encoding = "utf-8"   #JSONLoader里没有这一项
# )
# loader = JSONLoader(
#     file_path = "./data/stus.json",
#     jq_schema=".[].name",
#     text_content=False       #告知jsonloader所抽取的内容不是字符串
#     # encoding = "utf-8"   #JSONLoader里没有这一项
# )
loader = JSONLoader(
    file_path = "./data/stu_json_lines.json",
    json_lines=True,
    jq_schema=".name",
    text_content=False       #告知jsonloader所抽取的内容不是字符串
    # encoding = "utf-8"   #JSONLoader里没有这一项
)

#批量加载 .load() -> [Doc, Doc, ...]
documents = loader.load()
# for document in documents:
#     print(type(document), document)
print(documents)

# #懒加载  .lazy_load()  迭代器[Doc]
# for document in loader.lazy_load():
#     print(type(document), document)