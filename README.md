# KIE Integrations

Agent integrations for the KIE document extraction API. Each package wraps the same underlying API — extract structured data from documents (images/PDFs) using a JSON schema — and exposes it in a format native to a particular agent framework or tool ecosystem.

## Integrations

| Package | Framework | Status |
|---------|-----------|--------|
| [`kie-core/`](kie-core/) | Shared Python client (sync + async) | Available |
| [`claude-skill/`](claude-skill/) | [Claude Code](https://docs.anthropic.com/en/docs/claude-code) Skill | Available |
| [`claude-plugin/`](claude-plugin/) | [Claude Code](https://docs.anthropic.com/en/docs/claude-code) Plugin | Available |
| [`mcp-server/`](mcp-server/) | [Model Context Protocol](https://modelcontextprotocol.io/) Server | Available |
| [`openai-function/`](openai-function/) | [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) | Available |
| [`langchain-tool/`](langchain-tool/) | [LangChain Tool](https://python.langchain.com/docs/concepts/tools/) | Available |
| [`custom-gpt/`](custom-gpt/) | [OpenAI Custom GPT](https://chatgpt.com/gpts) (GPT Store) | Available |

## Architecture

```
┌─────────────────────────────────────────────────────┐
│  Agent frameworks                                   │
│  ┌──────────┐ ┌────────────┐ ┌──────────────┐        │
│  │MCP Server│ │OpenAI Func │ │LangChain Tool│        │
│  └────┬─────┘ └─────┬──────┘ └──────┬───────┘        │
│       └──────────────┼───────────────┘                │
│                      ▼                               │
│              ┌──────────────┐                        │
│              │   kie-core   │  httpx (sync + async)  │
│              └──────┬───────┘                        │
└─────────────────────┼───────────────────────────────┘
                      ▼
              KIE Extraction API
              POST /v1/extract
```

The `claude-skill/` and `claude-plugin/` are self-contained (no dependency on `kie-core`) and use only the Python standard library.

## Quick start

### Install the workspace

```bash
uv sync --all-packages --all-extras
```

### Run all tests

```bash
uv run pytest kie-core/tests/ mcp-server/tests/ openai-function/tests/ langchain-tool/tests/ -v
```

### Use an integration

**MCP Server:**

```bash
uv run kie-mcp-server
```

**OpenAI Function:**

```python
from kie_openai import TOOLS, handle_tool_call
```

**LangChain Tool:**

```python
from kie_langchain import KIEExtractDocumentTool
tool = KIEExtractDocumentTool()
```

**Claude Code Skill:** Copy or symlink `claude-skill/` into your skills directory.

**Claude Code Plugin:** `claude --plugin-dir ./claude-plugin/doc-extractor`

**Custom GPT:** Follow the setup guide in [`custom-gpt/README.md`](custom-gpt/README.md) to publish to the GPT Store.

## KIE API

All integrations call the same REST endpoint:

```
POST /v1/extract
```

**Request body:**

```json
{
  "document": { "content": "<base64>", "type": "pdf|image" },
  "schema": {
    "vendor_name": "string",
    "invoice_date": "date (MM/DD/YYYY)",
    "total_amount": "number"
  },
  "options": { "model": "<model_id>" }
}
```

**Response:** JSON object with extracted field values matching the schema keys.

### Schema format

Schemas are flat JSON objects where keys are field names and values are type hints:

- `"string"` — free-form text
- `"number"` — numeric value
- `"date (FORMAT)"` — date with format hint, e.g. `"date (MM/DD/YYYY)"`
- `"boolean"` — true/false
- `"currency"` — monetary amount
- Arrays of objects for tables/line items
- Any descriptive hint, e.g. `"5-digit zip code"`

See [`claude-skill/references/example_schemas.md`](claude-skill/references/example_schemas.md) for ready-made schemas for invoices, receipts, W-2s, bills of lading, and purchase orders.

## Configuration

Set the `KIE_API_URL` environment variable to point to your extraction service:

```bash
export KIE_API_URL=https://your-kie-service.example.com/v1/extract
```

Defaults to `http://localhost:8000/v1/extract` when not set.

## Repository structure

```
kie-integrations/
├── kie-core/                # Shared Python client library
│   ├── src/kie_core/
│   │   ├── client.py        #   Sync + async API client (httpx)
│   │   ├── document.py      #   Document encoding
│   │   └── schema.py        #   Schema loading
│   └── tests/
├── claude-skill/            # Claude Code skill (standalone, stdlib only)
│   ├── SKILL.md
│   ├── scripts/extract.py
│   └── references/
├── claude-plugin/           # Claude Code plugin (skill + MCP tool)
│   └── doc-extractor/
│       ├── skills/extract/
│       ├── scripts/mcp-server.py
│       └── .mcp.json
├── mcp-server/              # MCP server (FastMCP)
│   ├── src/kie_mcp_server/
│   └── tests/
├── openai-function/         # OpenAI function definition + handler
│   ├── src/kie_openai/
│   └── tests/
├── langchain-tool/          # LangChain BaseTool wrapper
│   ├── src/kie_langchain/
│   └── tests/
├── custom-gpt/              # Custom GPT for the OpenAI GPT Store
│   ├── openapi.yaml         #   OpenAPI spec (Action)
│   └── system_prompt.md     #   GPT system instructions
├── pyproject.toml           # uv workspace root
└── README.md
```

## Contributing

Each integration lives in its own top-level directory. When adding a new integration:

1. Create a new directory named `<framework>-<format>/` (e.g. `mcp-server/`).
2. Add a `pyproject.toml` with `kie-core` as a workspace dependency.
3. Include its own README with installation, usage, and testing instructions.
4. Use `KIE_API_URL` for endpoint configuration to stay consistent.
5. Add the package to the workspace `members` list in the root `pyproject.toml`.
6. Write tests — see existing packages for patterns.

## License

See [LICENSE](LICENSE) for details.
