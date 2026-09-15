# 🤖 AI Document Assistant — Streamlit RAG

A beginner-friendly RAG application that lets users upload **PDF, Excel, CSV,
DOCX, and images** and ask questions about the uploaded content.

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

The original project started an MCP server as a local `python` subprocess for
every question. That is fragile on hosted Streamlit environments. The deployed
version keeps the same `search_document` tool boundary in
`mcp_tools/context_tool.py`, but calls it directly inside the Streamlit process.

The original standalone MCP server remains in `mcp_tools/server.py` for local
experimentation and is not installed as a deployment dependency.

## Deploy on Streamlit Community Cloud

Streamlit Community Cloud uses `requirements.txt` for Python dependencies.
The entrypoint is `app.py`.

### 1. Upload this project to GitHub

Create a repository and push the contents of this folder.

### 2. Create the app

In Streamlit Community Cloud, choose the GitHub repository and set:

- Branch: `main`
- Main file path: `app.py`
- Python: 3.12

### 3. Add secrets

In the app's **Settings → Secrets**, add:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
OPENAI_API_KEY = "your_openai_api_key"
```

You only need the key for the model you use.

### Local run

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
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

- Gemini is the recommended default.
- The Gemini chat model is `gemini-2.5-flash`.
- Gemini text embeddings use `gemini-embedding-001`.
- FAISS is an in-memory vector store, so uploaded documents are re-indexed
  when the Streamlit session needs them again.
- Image OCR uses the selected multimodal model instead of EasyOCR/Tesseract,
  which avoids system-level OCR dependencies and makes cloud deployment easier.
- Scanned/image-only PDFs still need a separate PDF OCR pipeline; normal
  text-based PDFs work directly.

## Project structure

```text
.
├── app.py
├── config.py
├── requirements.txt
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
