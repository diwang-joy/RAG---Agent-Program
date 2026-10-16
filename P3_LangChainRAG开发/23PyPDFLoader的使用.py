from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = PyPDFLoader(
    file_path = "./data/PDF1.pdf",
    mode='page',          #读取模式，page（按页面划分不同document）和single（单个document）
    # password='passwprd',  #文件密码
)

#批量加载 .load() -> [Doc, Doc, ...]
# documents = loader.load()
# for document in documents:
#     print(type(document), document)
# print(documents)

#懒加载  .lazy_load()  迭代器[Doc]
i=0
for document in loader.lazy_load():
    i+=1
    print(type(document), document)
    print(i)