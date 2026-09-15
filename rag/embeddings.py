from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from config import (
    OPENAI_API_KEY,
    GEMINI_API_KEY,
    OPENAI_EMBEDDING_MODEL,
    GEMINI_EMBEDDING_MODEL,
)


def get_embedding_model(model_name: str):
    if model_name == "OpenAI":
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not configured.")
        return OpenAIEmbeddings(
            api_key=OPENAI_API_KEY,
            model=OPENAI_EMBEDDING_MODEL,
        )

    if model_name == "Gemini":
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not configured.")
        return GoogleGenerativeAIEmbeddings(
            google_api_key=GEMINI_API_KEY,
            model=GEMINI_EMBEDDING_MODEL,
        )

    raise ValueError("Invalid model selected.")
