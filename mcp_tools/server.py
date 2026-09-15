"""
Optional local MCP server.

This file is not required by the Streamlit deployment. It is kept so the
original project can still demonstrate the MCP tool separately when the MCP
package is installed locally.
"""

try:
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP("Document Assistant")

    @mcp.tool()
    def search_document(context: str) -> str:
        return context

    if __name__ == "__main__":
        mcp.run()
except ImportError:
    if __name__ == "__main__":
        raise SystemExit(
            "Install the optional MCP dependency to run this local server."
        )
