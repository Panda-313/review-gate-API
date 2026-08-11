from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import DOCUMENT_GLOB_PATTERN, RAW_DATA_PATH, CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL_NAME, \
    CHROMA_DB_PATH, CHROMA_COLLECTION_NAME


def load_documents(data_path: str | Path) -> list[Document]:
    data_path = Path(data_path)

    if not data_path.exists():
        raise FileNotFoundError(f"{data_path} does not exist")

    loader = DirectoryLoader(
        path=str(data_path),
        glob=DOCUMENT_GLOB_PATTERN,
        loader_cls=TextLoader
    )

    documents = loader.load()

    if not documents:
        raise FileNotFoundError(f"No files found in {data_path}")

    return documents


def split_documents(documents: list[Document]) -> list[Document]:
    if not documents:
        raise ValueError("No documents found")

    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

    chunks = splitter.split_documents(documents)

    return chunks


def create_vectorstore(chunks: list[Document]):
    if not chunks:
        raise ValueError("No chunks found")

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DB_PATH),
        collection_name=CHROMA_COLLECTION_NAME
    )

    return vectorstore

def ingest_search_knowledge() -> list[Document]:
    documents = load_documents(RAW_DATA_PATH)
    chunks = split_documents(documents)
    vectorstore = create_vectorstore(chunks)


    print(f"Zaladowano : {len(documents)} dokumentow")
    print(f"Zaladowano : {len(chunks)} chunkow")

    return documents


def main() -> None:
    ingest_search_knowledge()


if __name__ == "__main__":
    main()
