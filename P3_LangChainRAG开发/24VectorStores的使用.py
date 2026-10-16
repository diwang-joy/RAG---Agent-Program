from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader

vector_store = InMemoryVectorStore(
    embedding = DashScopeEmbeddings()
)

loader = CSVLoader(
    file_path = "./data/stu.csv",
    encoding = "utf-8",
    # csv_args = {
    #     "delimiter": ",",     #指定分隔符
    #     "quotechar": '"',
    #     "fieldnames": ['a','b','c','d'] #指定表头
    # }
    source_column="name"
)

#批量加载 .load() -> [Doc, Doc, ...]
documents = loader.load()
# print(documents[1])
# for document in documents:
#     print(type(document), document)

# #懒加载  .lazy_load()  迭代器[Doc]
# for document in loader.lazy_load():
#     print(type(document), document)

#向量存储的增删查
vector_store.add_documents(
    documents=documents,         #被添加的文档，类型：list[doc]
    ids=["id"+str(i) for i in range(1,len(documents)+1)],   #给添加的文档提供id（字符串） list[str]                    
)

#删除 传入[id,id...]
vector_store.delete(["id1", "id2"])

#查
res = vector_store.similarity_search(
    "dy",
    3                 #检索的结果要几个
)

print(res)