# KIE Document Extractor — Claude Code Plugin

A [Claude Code Plugin](https://code.claude.com/docs/en/plugins) that adds document extraction capabilities to Claude Code. Provides both a skill (guided extraction workflow) and an MCP tool (direct `extract_document` tool access).

## What's included

| Component | Description |
|-----------|-------------|
| **Skill** `/doc-extractor:extract` | Guided workflow — collects inputs, builds schema, runs extraction, reviews results |
| **MCP tool** `extract_document` | Direct tool — Claude can call extraction programmatically during any conversation |

Both components are fully self-contained with zero external Python dependencies (the MCP server uses PEP 723 inline metadata so `uv run` handles the `mcp` package automatically).

## Installation

### Local testing

```bash
claude --plugin-dir ./claude-plugin/doc-extractor
```

### Install to user scope

Add the plugin directory to a [marketplace](https://code.claude.com/docs/en/plugin-marketplaces), then:

```bash
claude plugin install doc-extractor@<marketplace>
```

## Usage

### Via the skill

```
/doc-extractor:extract
```

Claude will ask for a document and what fields to extract, then handle everything automatically. You can also provide arguments directly:

```
/doc-extractor:extract invoice.pdf — extract vendor name, date, and total
```

### Via the MCP tool

Once the plugin is loaded, Claude has access to the `extract_document` tool and will use it automatically when you ask to extract data from a document.

## Plugin structure

```
doc-extractor/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── skills/
│   └── extract/
│       ├── SKILL.md             # Skill definition
│       ├── scripts/
│       │   └── extract.py       # Extraction script (stdlib only)
│       └── references/
│           └── example_schemas.md
├── .mcp.json                    # MCP server configuration
├── scripts/
│   └── mcp-server.py            # MCP server (PEP 723 inline deps)
└── README.md
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `KIE_API_URL` | KIE extraction API endpoint | `http://localhost:8000/v1/extract` |

## Supported documents

- **Images:** PNG, JPG, TIFF, BMP, WebP
- **PDFs:** single- and multi-page

## Schema format

Schemas define the fields to extract. Keys are field names; values are type hints:

```json
{
  "vendor_name": "string",
  "invoice_date": "date (MM/DD/YYYY)",
  "total_amount": "number",
  "line_items": [{"description": "string", "qty": "number", "price": "number"}]
}
```

See [`skills/extract/references/example_schemas.md`](doc-extractor/skills/extract/references/example_schemas.md) for ready-made schemas for invoices, receipts, W-2s, bills of lading, and purchase orders.

See the [root README](../README.md) for full API and schema format details.
