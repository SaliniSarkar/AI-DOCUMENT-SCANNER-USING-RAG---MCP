from PIL import Image
from google import genai
from google.genai import types
from langchain_openai import ChatOpenAI

from config import (
    GEMINI_API_KEY,
    GEMINI_CHAT_MODEL,
    OPENAI_API_KEY,
    OPENAI_CHAT_MODEL,
)


def load_image(uploaded_file, model_name="Gemini"):
    """Extract readable text from an image using a multimodal model."""
    image = Image.open(uploaded_file).convert("RGB")

    prompt = (
        "Extract all readable text from this image. "
        "Preserve the logical order and return only the extracted text. "
        "Do not summarize or explain."
    )

    if model_name == "Gemini":
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required for image OCR.")

        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model=GEMINI_CHAT_MODEL,
            contents=[prompt, image],
            config=types.GenerateContentConfig(temperature=0),
        )
        return (getattr(response, "text", None) or "").strip()

    if model_name == "OpenAI":
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required for image OCR.")

        # Convert PIL image to a data URL for OpenAI's multimodal input.
        import base64
        from io import BytesIO

        buffer = BytesIO()
        image.save(buffer, format="PNG")
        image_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model=OPENAI_CHAT_MODEL,
            temperature=0,
        )
        response = llm.invoke(
            [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_b64}"
                            },
                        },
                    ],
                }
            ]
        )
        return str(response.content).strip()

    raise ValueError("Invalid model selected.")
