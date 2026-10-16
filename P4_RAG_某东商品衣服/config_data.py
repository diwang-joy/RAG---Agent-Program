
md5_path = "E:\code\AI Agent Program\P4_RAG_某东商品衣服\md5.text"

#Chroma
collection_name = "rag"
persist_directory = "E:\code\AI Agent Program\P4_RAG_某东商品衣服\chroma_db"

#Splitter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", ".", "。", ",", "，", "?", "？", "!", " ", ""]
max_split_char_number = 1000

#
similarity_search_threshold = 2

#chatModel
chat_model = "qwen3-max-2026-01-23"

#session_id配置
session_config = {
    "configurable": {
        "session_id": "user_001",
    }
}