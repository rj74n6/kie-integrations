# KIE Document Extractor — Claude Code Plugin

A [Claude Code Plugin](https://docs.anthropic.com/en/docs/claude-code) that registers document extraction as a tool Claude can invoke during conversations.

## Overview

This plugin exposes the KIE document extraction API as a native Claude Code tool. When registered, Claude can call the `doc-extractor` tool to extract structured data from documents using a JSON schema — without the user needing to run any scripts manually.

## Installation

Copy the plugin directory into your project:

```bash
cp -r claude-plugin/doc-extractor /path/to/your-project/
```

Or register it as a plugin in your Claude Code configuration.

## Plugin manifest

The plugin is defined in `doc-extractor/.claude-plugin/plugin.json`:

```json
{
  "name": "doc-extractor",
  "description": "Extract structured data from documents using a KIE API",
  "version": "1.0.0"
}
```

## Usage

Once registered, Claude will automatically have access to the `doc-extractor` tool. Ask Claude to extract data from any supported document:

> "Extract the vendor name, invoice number, and line items from this PDF."

Claude will invoke the plugin, which calls the KIE extraction API and returns structured JSON results.

## File structure

```
claude-plugin/
├── README.md                       # This file
└── doc-extractor/
    └── .claude-plugin/
        └── plugin.json             # Plugin manifest
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

See the [root README](../README.md) for the full schema format and API details.
