from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader(
    file_path = "./data/TextLoader.txt",
    encoding = "utf-8" 
)

#批量加载 .load() -> [Doc, Doc, ...]
documents = loader.load()
# for document in documents:
#     print(type(document), document)
# print(documents)

# #懒加载  .lazy_load()  迭代器[Doc]
# for document in loader.lazy_load():
#     print(type(document), document)

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50,
    separators=["\n\n", "\n", ".", "。", ",", "，", "?", "？", "!", ""],
    length_function=len
)

split_docs = splitter.split_documents(documents)
print(len(split_docs))
for s in split_docs:
    print(s)