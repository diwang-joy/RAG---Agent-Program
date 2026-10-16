from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path = "./data/stu.csv",
    encoding = "utf-8",
    csv_args = {
        "delimiter": ",",     #指定分隔符
        "quotechar": '"',
        "fieldnames": ['a','b','c','d'] #指定表头
    }
)

#批量加载 .load() -> [Doc, Doc, ...]
documents = loader.load()
# for document in documents:
#     print(type(document), document)

#懒加载  .lazy_load()  迭代器[Doc]
for document in loader.lazy_load():
    print(type(document), document)