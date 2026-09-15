def search_document(context: str) -> str:
    """
    Deployment-safe equivalent of the original MCP search_document tool.

    The original project started a local stdio MCP server for every question.
    That pattern is unnecessary for a Streamlit deployment and can fail in
    hosted environments. Keeping the tool logic as a normal Python function
    preserves the tool boundary without spawning a subprocess.
    """
    return context
