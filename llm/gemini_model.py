from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_CHAT_MODEL


FALLBACK = "SORRY 🙂 I couldn't find that information in the uploaded document."


def _client():
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=GEMINI_API_KEY)


def ask_gemini(context: str, question: str) -> str:
    client = _client()

    prompt = f"""
You are a helpful document assistant.

Answer the user's question using ONLY the supplied document context.
Do not invent facts or use outside knowledge.
If the context does not contain the answer, reply exactly:
{FALLBACK}

Document context:
{context}

User question:
{question}
"""

    response = client.models.generate_content(
        model=GEMINI_CHAT_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0,
            max_output_tokens=2048,
        ),
    )

    text = getattr(response, "text", None)
    if not text:
        return FALLBACK
    return text.strip()
