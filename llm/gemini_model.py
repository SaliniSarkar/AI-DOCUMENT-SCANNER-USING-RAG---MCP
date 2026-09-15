from langchain_google_genai import ChatGoogleGenerativeAI

from config import GEMINI_API_KEY, GEMINI_CHAT_MODEL


FALLBACK = "SORRY 🙂 I couldn't find that information in the uploaded document."


def _content_to_text(content) -> str:
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                text = block.get("text")
                if text:
                    parts.append(text)
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts)

    return str(content)


def ask_gemini(context: str, question: str) -> str:
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not configured.")

    llm = ChatGoogleGenerativeAI(
        google_api_key=GEMINI_API_KEY,
        model=GEMINI_CHAT_MODEL,
        temperature=0,
    )

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

    response = llm.invoke(prompt)
    return _content_to_text(response.content).strip()
