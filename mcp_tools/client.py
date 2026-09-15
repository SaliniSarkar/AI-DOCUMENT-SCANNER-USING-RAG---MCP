"""
Legacy MCP client kept for local experiments.

The deployed Streamlit app does NOT start a subprocess-based MCP server.
See mcp_tools/context_tool.py and app.py.
"""

async def get_context(context: str) -> str:
    from mcp_tools.context_tool import search_document
    return search_document(context)
