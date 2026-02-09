#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<'EOF'
Usage: ./start.sh [options]

Start the KIE Document Extractor MCP server.

Options:
  --transport <mode>   Transport mode: "streamable-http" (default) or "stdio"
  --host <address>     Bind address for HTTP mode (default: 0.0.0.0)
  --port <port>        Listen port for HTTP mode (default: 8080)
  --api-url <url>      KIE extraction API endpoint
                       (default: http://localhost:8000/v1/extract)
  -h, --help           Show this help message

Environment variables (override defaults, overridden by flags):
  MCP_TRANSPORT, MCP_HOST, MCP_PORT, KIE_API_URL

Examples:
  # Streamable HTTP transport (default — for Claude.ai connectors)
  ./start.sh

  # stdio transport (for Cursor, Claude Code, Claude Desktop)
  ./start.sh --transport stdio

  # Custom API endpoint and port
  ./start.sh --transport streamable-http --port 9090 --api-url https://kie.example.com/v1/extract
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --transport)
      export MCP_TRANSPORT="$2"
      shift 2
      ;;
    --host)
      export MCP_HOST="$2"
      shift 2
      ;;
    --port)
      export MCP_PORT="$2"
      shift 2
      ;;
    --api-url)
      export KIE_API_URL="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Error: unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

transport="${MCP_TRANSPORT:-streamable-http}"
echo "Starting KIE MCP server (transport=${transport}) ..."

exec uv run --project "$SCRIPT_DIR" kie-mcp-server
