import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Streamlit Community Cloud: add these in App Settings -> Secrets.
# Local development: use .streamlit/secrets.toml or .env.
def get_api_key(provider: str):
    env_name = f"{provider.upper()}_API_KEY"

    try:
        value = st.secrets.get(env_name)
    except Exception:
        value = None

    return value or os.getenv(env_name)


OPENAI_API_KEY = get_api_key("OpenAI")
GEMINI_API_KEY = get_api_key("Gemini")

OPENAI_CHAT_MODEL = "gpt-4.1-mini"
GEMINI_CHAT_MODEL = "gemini-2.5-flash"

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
GEMINI_EMBEDDING_MODEL = "gemini-embedding-001"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
TOP_K = 4

SUPPORTED_FILES = {
    "📄 PDF": ["pdf"],
    "📊 Excel": ["xlsx", "xls"],
    "📝 CSV": ["csv"],
    "📑 DOCX": ["docx"],
    "🖼️ Image OCR": ["png", "jpg", "jpeg"],
}
