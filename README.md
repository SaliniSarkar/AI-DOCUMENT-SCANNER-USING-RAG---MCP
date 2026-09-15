# 🤖 AI Document Assistant — Streamlit RAG

A beginner-friendly RAG application that lets users upload **PDF, Excel, CSV,
DOCX, and images** and ask questions about the uploaded content.

## Deployment fixes included

This version is prepared for **Streamlit Community Cloud** and removes the
legacy Gemini Python SDK that caused this warning:

> `google.generativeai` package has ended support

The project now uses Google's current `google-genai` SDK directly for:

- Gemini text generation
- Gemini multimodal image OCR
- Gemini embeddings (`gemini-embedding-001`)

The LangChain Gemini integration is intentionally not used, because older
versions of that integration import the deprecated `google.generativeai`
package and can produce the warning shown in Streamlit Cloud logs.

The project also targets **Python 3.12**. Streamlit Community Cloud currently
defaults to Python 3.12, while your log showed Python 3.10.21. The `runtime.txt`
and `.python-version` files document the intended version, but when creating
a new Community Cloud deployment you should explicitly choose **Python 3.12**
in Advanced settings. Streamlit documents that Python version is selected at
deployment time and changing it later requires redeploying the app.

## Architecture

1. Upload document
2. Extract text / OCR
3. Split text into chunks
4. Create embeddings
5. Store vectors in FAISS
6. Retrieve the most relevant chunks
7. Pass retrieved context to Gemini or OpenAI
8. Generate a grounded answer

### MCP change for deployment

The original project started an MCP server as a local Python subprocess for
every question. That is fragile on hosted Streamlit environments. The deployed
version keeps the same `search_document` tool boundary in
`mcp_tools/context_tool.py`, but calls it directly inside the Streamlit process.

The standalone MCP server remains in `mcp_tools/server.py` for local
experimentation and is not a runtime dependency of the Streamlit app.

## Deploy on Streamlit Community Cloud

### 1. Push the project to GitHub

Create a repository and push the contents of this folder. `app.py` and
`requirements.txt` must be in the repository root.

### 2. Create the Streamlit app

In Streamlit Community Cloud:

- Repository: your GitHub repository
- Branch: `main`
- Main file path: `app.py`
- **Advanced settings → Python version: 3.12**

If an existing app was already deployed with Python 3.10, delete and redeploy
it with Python 3.12; Streamlit does not let you change the Python version of an
existing deployment in place.

### 3. Add secrets

In **App Settings → Secrets**, add:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
OPENAI_API_KEY = "your_openai_api_key"
```

You only need the key for the model you use. Do not commit real API keys to
GitHub.

### Local run

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

For local secrets, create `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
OPENAI_API_KEY = "your_openai_api_key"
```

Do not commit that file.

## Important notes

- **Gemini is the recommended default.**
- Gemini chat model: `gemini-2.5-flash`.
- Gemini embedding model: `gemini-embedding-001`.
- The project uses `google-genai`, not the deprecated `google-generativeai`.
- FAISS is an in-memory vector store. Uploaded documents are indexed for the
  current Streamlit session.
- Image OCR uses the selected multimodal model instead of EasyOCR/Tesseract,
  avoiding system-level OCR dependencies.
- Normal text-based PDFs work directly. Scanned/image-only PDFs need a
  dedicated PDF OCR pipeline if you want OCR inside PDFs as well.

## Expected Streamlit logs

You should no longer see:

```text
FutureWarning: You are using a Python version (3.10...)
FutureWarning: All support for the `google.generativeai` package has ended
```

If the first warning still appears, the deployed app is still running Python
3.10 and needs to be redeployed with Python 3.12.

If the second warning still appears, an old dependency is still being installed.
Make sure the deployed repository uses the updated `requirements.txt` from this
package and does not contain another `requirements.txt`, `pyproject.toml`,
`Pipfile`, or `uv.lock` that Streamlit could select instead. Streamlit uses the
first recognized dependency file it finds.

## Project structure

```text
.
├── app.py
├── config.py
├── requirements.txt
├── runtime.txt
├── .python-version
├── .env.example
├── .gitignore
├── .streamlit/
│   └── config.toml
├── loaders/
│   ├── loader.py
│   ├── pdf_loader.py
│   ├── docx_loader.py
│   ├── excel_loader.py
│   ├── csv_loader.py
│   └── image_loader.py
├── rag/
│   ├── embeddings.py
│   ├── vector_store.py
│   └── retriever.py
├── llm/
│   ├── model.py
│   ├── gemini_model.py
│   └── openai_model.py
└── mcp_tools/
    ├── context_tool.py
    ├── client.py
    └── server.py
```
