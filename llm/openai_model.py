from langchain_openai import ChatOpenAI

from config import OPENAI_API_KEY, OPENAI_CHAT_MODEL


FALLBACK = "SORRY 🙂 I couldn't find that information in the uploaded document."


def ask_openai(context: str, question: str) -> str:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not configured.")

    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=OPENAI_CHAT_MODEL,
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
    return str(response.content).strip()
