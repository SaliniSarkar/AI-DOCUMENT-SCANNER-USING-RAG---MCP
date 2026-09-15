import hashlib
import streamlit as st

from config import SUPPORTED_FILES, get_api_key
from loaders.loader import load_document
from rag.vector_store import create_vector_store
from rag.retriever import retrieve_context
from llm.model import ask_llm
from mcp_tools.context_tool import search_document

st.set_page_config(
    page_title="AI Document Assistant",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AI Document Assistant")
st.caption("RAG-powered document Q&A for PDF, Excel, CSV, DOCX and image OCR.")

# ---------------- Session state ----------------
defaults = {
    "messages": [],
    "vector_store": None,
    "document_id": None,
    "document_name": None,
    "document_text": None,
    "selected_model": "Gemini",
    "selected_assistant": "📄 PDF",
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("⚙️ Settings")

    model = st.selectbox(
        "AI Model",
        ["Gemini", "OpenAI"],
        index=["Gemini", "OpenAI"].index(st.session_state.selected_model),
        help="Gemini is recommended for this deployment.",
    )
    st.session_state.selected_model = model

    assistant = st.selectbox(
        "Document Type",
        list(SUPPORTED_FILES.keys()),
        index=list(SUPPORTED_FILES.keys()).index(st.session_state.selected_assistant),
    )
    st.session_state.selected_assistant = assistant

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ---------------- API-key validation ----------------
if not get_api_key(model):
    st.warning(
        f"Please configure the `{model.upper()}_API_KEY` secret before using the {model} model."
    )

# ---------------- Upload ----------------
uploaded_file = st.file_uploader(
    "📑 Upload a document",
    type=SUPPORTED_FILES[assistant],
    help="For best results, use text-based PDFs and clear images.",
)

if uploaded_file is not None:
    raw_bytes = uploaded_file.getvalue()
    document_id = hashlib.sha256(
        raw_bytes + model.encode("utf-8") + assistant.encode("utf-8")
    ).hexdigest()

    if st.session_state.document_id != document_id:
        try:
            with st.spinner("Reading and indexing document... ⏳"):
                text = load_document(uploaded_file, model_name=model)

                if not text or not text.strip():
                    raise ValueError(
                        "No readable text was found. Try another file or a text-based PDF."
                    )

                vector_store = create_vector_store(text, model)

            st.session_state.vector_store = vector_store
            st.session_state.document_id = document_id
            st.session_state.document_name = uploaded_file.name
            st.session_state.document_text = text
            st.session_state.messages = []

            st.success(f"✅ {uploaded_file.name} is ready.")
        except Exception as exc:
            st.session_state.vector_store = None
            st.error(f"Could not process the document: {exc}")

elif st.session_state.document_name:
    st.info(f"Current document: **{st.session_state.document_name}**")

# ---------------- Chat history ----------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- Chat input ----------------
question = st.chat_input("Ask a question about your uploaded document...")

if question:
    if st.session_state.vector_store is None:
        st.warning("Please upload and process a document first.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    try:
        with st.chat_message("assistant"):
            with st.spinner("Searching the document and generating an answer..."):
                retrieved_context = retrieve_context(
                    st.session_state.vector_store, question
                )

                # Deployment-safe MCP-compatible tool layer.
                # The Streamlit app calls the same tool logic directly instead
                # of starting a local stdio MCP subprocess.
                context = search_document(retrieved_context)

                answer = ask_llm(model, context, question)
                st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )
    except Exception as exc:
        error_message = f"Something went wrong: {exc}"
        st.error(error_message)
        st.session_state.messages.append(
            {"role": "assistant", "content": error_message}
        )
