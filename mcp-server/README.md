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

### stdio transport (default)

For local MCP clients (Claude Code, Cursor, Claude Desktop, etc.):

```bash
# Run directly
uv run kie-mcp-server

# Or as a module
uv run python -m kie_mcp_server
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

### Streamable HTTP transport (remote)

For remote access from Claude.ai connectors:

```bash
MCP_TRANSPORT=streamable-http uv run kie-mcp-server
```

The server listens at `http://0.0.0.0:8080/mcp` by default.

#### Environment variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MCP_TRANSPORT` | Transport mode (`stdio` or `streamable-http`) | `stdio` |
| `MCP_HOST` | Bind address (HTTP mode only) | `0.0.0.0` |
| `MCP_PORT` | Listen port (HTTP mode only) | `8080` |
| `KIE_API_URL` | KIE extraction API endpoint | `http://localhost:8000/v1/extract` |

### Claude.ai custom connector

To add this MCP server as a custom connector on Claude.ai:

1. Deploy the server behind an HTTPS reverse proxy (see Caddy example below).
2. Go to **Claude.ai → Settings → Connectors → Add custom connector**.
3. Fill in:
   - **Name:** KIE Document Extractor
   - **Remote MCP server URL:** `https://your-domain.com/mcp`
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
KIE_API_URL=http://localhost:8000/v1/extract \
MCP_TRANSPORT=streamable-http \
  uv run kie-mcp-server
```

## File structure

```
mcp-server/
├── README.md
├── pyproject.toml
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
