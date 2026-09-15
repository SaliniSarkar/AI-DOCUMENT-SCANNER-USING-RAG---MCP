from config import TOP_K


def retrieve_context(vector_store, question: str) -> str:
    if vector_store is None:
        raise ValueError("Vector store is not initialized.")

    documents = vector_store.similarity_search(question, k=TOP_K)
    return "\n\n".join(doc.page_content for doc in documents)
