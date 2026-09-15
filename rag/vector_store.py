from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import CHUNK_OVERLAP, CHUNK_SIZE
from rag.embeddings import get_embedding_model


def create_vector_store(text: str, model_name: str):
    if not text or not text.strip():
        raise ValueError("The document contains no readable text.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = splitter.split_text(text)
    if not chunks:
        raise ValueError("No text chunks were created.")

    embedding_model = get_embedding_model(model_name)
    return FAISS.from_texts(chunks, embedding_model)
