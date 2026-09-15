from typing import List

from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings
from google import genai
from google.genai import types

from config import (
    OPENAI_API_KEY,
    GEMINI_API_KEY,
    OPENAI_EMBEDDING_MODEL,
    GEMINI_EMBEDDING_MODEL,
)


class GeminiEmbeddings(Embeddings):
    """LangChain-compatible embeddings using the modern google-genai SDK."""

    def __init__(self, api_key: str, model: str = GEMINI_EMBEDDING_MODEL):
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def _embed(self, texts: List[str], task_type: str) -> List[List[float]]:
        if not texts:
            return []

        result = self.client.models.embed_content(
            model=self.model,
            contents=texts,
            config=types.EmbedContentConfig(task_type=task_type),
        )

        return [list(embedding.values) for embedding in result.embeddings]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self._embed(texts, "RETRIEVAL_DOCUMENT")

    def embed_query(self, text: str) -> List[float]:
        return self._embed([text], "RETRIEVAL_QUERY")[0]


def get_embedding_model(model_name: str):
    if model_name == "OpenAI":
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not configured.")
        return OpenAIEmbeddings(
            api_key=OPENAI_API_KEY,
            model=OPENAI_EMBEDDING_MODEL,
        )

    if model_name == "Gemini":
        return GeminiEmbeddings(
            api_key=GEMINI_API_KEY,
            model=GEMINI_EMBEDDING_MODEL,
        )

    raise ValueError("Invalid model selected.")
