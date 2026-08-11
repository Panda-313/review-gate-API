from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from src.config import EMBEDDING_MODEL_NAME, CHROMA_DB_PATH, CHROMA_COLLECTION_NAME

def load_vectorstore() -> Chroma:
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    return Chroma(
        persist_directory=str(CHROMA_DB_PATH),
        collection_name=CHROMA_COLLECTION_NAME,
        embedding_function=embeddings,
    )
