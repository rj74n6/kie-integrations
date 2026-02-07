"""Entry point for ``python -m kie_mcp_server``."""

from kie_mcp_server.server import server


def main() -> None:
    """Run the MCP server over stdio."""
    server.run()


if __name__ == "__main__":
    main()
