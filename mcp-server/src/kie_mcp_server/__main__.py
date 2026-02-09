"""Entry point for ``python -m kie_mcp_server``."""

import os

from kie_mcp_server.server import server


def main() -> None:
    """Run the MCP server.

    Transport is selected via the ``MCP_TRANSPORT`` environment variable:

    - ``stdio`` (default) — for local MCP clients (Claude Code, Cursor, etc.)
    - ``streamable-http`` — for remote access from Claude.ai connectors
    """
    transport = os.environ.get("MCP_TRANSPORT", "stdio")

    if transport == "streamable-http":
        host = os.environ.get("MCP_HOST", "0.0.0.0")
        port = int(os.environ.get("MCP_PORT", "8080"))
        server.run(transport="streamable-http", host=host, port=port)
    else:
        server.run()


if __name__ == "__main__":
    main()
