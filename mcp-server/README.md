# KIE Document Extractor — MCP Server

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that exposes KIE document extraction as a tool any MCP-compatible client can call.

## Installation

```bash
uv sync --package kie-mcp-server
```

## Tool: `extract_document`

Extract structured data from a document using a JSON schema.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `document_path` | `string` | Yes | Path to the document (PDF or image) |
| `schema` | `object` | Yes | JSON schema defining the fields to extract |
| `model` | `string` | No | Model ID for extraction |

**Returns:** JSON string with extracted field values.

## Usage

### stdio transport

```bash
# Run directly
uv run kie-mcp-server

# Or as a module
uv run python -m kie_mcp_server
```

### Configuration in MCP clients

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

## File structure

```
mcp-server/
├── README.md
├── pyproject.toml
├── src/
│   └── kie_mcp_server/
│       ├── __init__.py
│       ├── __main__.py          # Entry point
│       └── server.py            # FastMCP server + tool definition
└── tests/
    ├── conftest.py
    └── test_server.py
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `KIE_API_URL` | KIE extraction API endpoint | `http://localhost:8000/v1/extract` |

## Dependencies

- `kie-core` — shared extraction client (workspace dependency)
- `mcp` — Model Context Protocol Python SDK

## Testing

```bash
uv run pytest mcp-server/tests/ -v
```
