"""Entry point for ``python -m kie_mcp_server``."""

import os

from mcp.server.transport_security import TransportSecuritySettings

from kie_mcp_server.server import server


def main() -> None:
    """Run the MCP server.

    Transport is selected via the ``MCP_TRANSPORT`` environment variable:

    - ``stdio`` (default) — for local MCP clients (Claude Code, Cursor, etc.)
    - ``streamable-http`` — for remote access from Claude.ai connectors
    """
    transport = os.environ.get("MCP_TRANSPORT", "stdio")

    if transport == "streamable-http":
        server.settings.host = os.environ.get("MCP_HOST", "0.0.0.0")
        server.settings.port = int(os.environ.get("MCP_PORT", "8080"))

        # Disable DNS rebinding protection when binding to all interfaces
        # (typically behind a reverse proxy like Caddy that handles this).
        server.settings.transport_security = TransportSecuritySettings(
            enable_dns_rebinding_protection=False,
        )

    server.run(transport=transport)


if __name__ == "__main__":
    main()
