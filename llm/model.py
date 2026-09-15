from llm.openai_model import ask_openai
from llm.gemini_model import ask_gemini


def ask_llm(model_name: str, context: str, question: str) -> str:
    if model_name == "OpenAI":
        return ask_openai(context, question)
    if model_name == "Gemini":
        return ask_gemini(context, question)
    raise ValueError("Invalid AI model selected.")
