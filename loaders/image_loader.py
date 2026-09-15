import base64
from io import BytesIO

from PIL import Image
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from config import (
    GEMINI_API_KEY,
    GEMINI_CHAT_MODEL,
    OPENAI_API_KEY,
    OPENAI_CHAT_MODEL,
)


def load_image(uploaded_file, model_name="Gemini"):
    """
    Cloud-friendly OCR.

    Instead of EasyOCR/Tesseract (which add large ML/system dependencies),
    the selected multimodal LLM reads the image and returns its text.
    """
    image = Image.open(uploaded_file).convert("RGB")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    image_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    image_message = {
        "type": "image_url",
        "image_url": {"url": f"data:image/png;base64,{image_b64}"},
    }

    prompt = (
        "Extract all readable text from this image. "
        "Preserve the logical order and return only the extracted text. "
        "Do not summarize or explain."
    )

    if model_name == "Gemini":
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required for image OCR.")
        llm = ChatGoogleGenerativeAI(
            google_api_key=GEMINI_API_KEY,
            model=GEMINI_CHAT_MODEL,
            temperature=0,
        )
    elif model_name == "OpenAI":
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required for image OCR.")
        llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model=OPENAI_CHAT_MODEL,
            temperature=0,
        )
    else:
        raise ValueError("Invalid model selected.")

    response = llm.invoke(
        [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    image_message,
                ],
            }
        ]
    )

    return str(response.content)
