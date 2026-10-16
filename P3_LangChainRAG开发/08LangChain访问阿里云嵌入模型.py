# #访问阿里云嵌入模型
# from langchain_community.embeddings import DashScopeEmbeddings

# #创建模型对象，不传model默认用的是 text-embeddings-v1
# model = DashScopeEmbeddings()

# #不用invoke stream
# #embed_query，embed_documents
# print(model.embed_query("我喜欢你"))
# print(model.embed_documents(["我喜欢你","LOVE","PASSION"]))

#访问Ollama的本地嵌入模型
from langchain_ollama.embeddings import OllamaEmbeddings

#创建模型对象，不传model默认用的是 text-embeddings-v1
model = OllamaEmbeddings(model="qwen3-embedding")

#不用invoke stream
#embed_query，embed_documents
print(model.embed_query("我喜欢你"))
print(model.embed_documents(["我喜欢你","LOVE","PASSION"]))