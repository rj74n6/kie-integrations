# KIE Document Extractor — MCP Server

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that exposes KIE document extraction as a tool any MCP-compatible client can call.

Supports both **stdio** (local) and **Streamable HTTP** (remote) transports, so it works with Claude Code, Cursor, Claude Desktop, and as a **Claude.ai custom connector**.

## Installation

```bash
uv sync --package kie-mcp-server
```

## Tool: `extract_document`

Extract structured data from a document using a JSON schema.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `document_content` | `string` | Yes | Base64-encoded document content |
| `document_type` | `string` | Yes | Document type — `"pdf"` or `"image"` |
| `schema` | `object` | Yes | JSON schema defining the fields to extract |
| `model` | `string` | No | Model ID for extraction |

**Returns:** JSON string with extracted field values.

## Usage

### Quick start

```bash
# Streamable HTTP (default) — listens at http://0.0.0.0:8080/mcp
./start.sh

# stdio transport — for local MCP clients (Cursor, Claude Code, Claude Desktop)
./start.sh --transport stdio

# Custom port and API endpoint
./start.sh --port 9090 --api-url https://kie.example.com/v1/extract
```

You can also run the server directly with `uv`:

```bash
# Streamable HTTP (set transport explicitly since uv bypasses start.sh defaults)
MCP_TRANSPORT=streamable-http uv run kie-mcp-server

# stdio
uv run kie-mcp-server
```

### Streamable HTTP transport (default)

The default transport for remote access from Claude.ai connectors and other HTTP-based clients. The server listens at `http://0.0.0.0:8080/mcp`.

### stdio transport

For local MCP clients (Claude Code, Cursor, Claude Desktop, etc.):

```bash
./start.sh --transport stdio
```

#### Configuration in MCP clients

```json
{
  "mcpServers": {
    "kie-doc-extractor": {
      "command": "uv",
      "args": ["run", "--project", "/path/to/kie-integrations/mcp-server", "kie-mcp-server"],
      "env": {
        "KIE_API_URL": "https://your-kie-service.example.com/v1/extract"
      }
    }
  }
}
```

### Environment variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MCP_TRANSPORT` | Transport mode (`streamable-http` or `stdio`) | `streamable-http` (`start.sh`) / `stdio` (`uv run`) |
| `MCP_HOST` | Bind address (HTTP mode only) | `0.0.0.0` |
| `MCP_PORT` | Listen port (HTTP mode only) | `8080` |
| `KIE_API_URL` | KIE extraction API endpoint | `http://localhost:8000/v1/extract` |

> **Note:** `start.sh` defaults `MCP_TRANSPORT` to `streamable-http`. When running via `uv run kie-mcp-server` directly, the Python entry point defaults to `stdio`.

### Claude.ai custom connector

To add this MCP server as a custom connector on Claude.ai:

1. Deploy the server behind an HTTPS reverse proxy (see Caddy example below).
2. Go to **Claude.ai → Settings → Connectors → Add custom connector**.
3. Fill in:
   - **Name:** KIE Document Extractor
   - **Remote MCP server URL:** `https://api.dillydally.dev/mcp`
   - Leave OAuth fields blank (not required).

#### Caddy reverse proxy example

If your KIE API is already served by Caddy, add the MCP endpoint alongside it:

```
your-domain.com {
    # Existing KIE API
    handle /v1/* {
        reverse_proxy localhost:8000
    }

    # MCP server for Claude.ai connector
    handle /mcp {
        reverse_proxy localhost:8080
    }
}
```

Then start the MCP server:

```bash
KIE_API_URL=http://localhost:8000/v1/extract ./start.sh
```

## File structure

```
mcp-server/
├── README.md
├── pyproject.toml
├── start.sh                       # Shell script to start the server
├── src/
│   └── kie_mcp_server/
│       ├── __init__.py
│       ├── __main__.py          # Entry point (stdio / streamable-http)
│       └── server.py            # FastMCP server + tool definition
└── tests/
    ├── conftest.py
    └── test_server.py
```

## Dependencies

- `kie-core` — shared extraction client (workspace dependency)
- `mcp` — Model Context Protocol Python SDK (includes `uvicorn`, `starlette`)

## Testing

```bash
uv run pytest mcp-server/tests/ -v
```
