# KIE Document Extractor — Claude Code Skill

A [Claude Code Skill](https://docs.anthropic.com/en/docs/claude-code) that enables Claude to extract structured data from documents (images and PDFs) by calling the KIE extraction API.

## Overview

When installed, Claude can accept a document and a description of the fields to extract, then automatically:

1. Build a JSON schema from the user's request
2. Call the KIE extraction API with the document and schema
3. Return the extracted fields as structured JSON

No external dependencies are required — the extraction script uses only the Python standard library.

## Installation

Copy or symlink this directory into your Claude Code skills directory:

```bash
# Example: symlink into your skills folder
ln -s /path/to/kie-integrations/claude-skill ~/.claude/skills/doc-extractor
```

## Usage

Once installed, simply ask Claude to extract data from a document:

> "Extract the vendor name, invoice date, and total from invoice.pdf"

Claude will use the skill to construct the schema, call the API, and return the results.

You can also provide an explicit JSON schema:

> "Extract fields from receipt.png using this schema: `{"store_name": "string", "total": "number"}`"

### Direct script usage

The extraction script can also be run standalone:

```bash
python3 scripts/extract.py <document_path> '<json_schema>' [-o output.json]
```

**Options:**

| Flag | Description |
|------|-------------|
| `-o, --output` | Save extracted JSON to a file |
| `--endpoint` | Override API endpoint (default: `$KIE_API_URL` or `http://localhost:8000/v1/extract`) |
| `--model` | Model ID for extraction (e.g. `joy-vl-3b-sglang`) |

**Example:**

```bash
python3 scripts/extract.py invoice.pdf \
  '{"vendor_name": "string", "total_amount": "number"}' \
  -o result.json
```

## File structure

```
claude-skill/
├── SKILL.md                        # Skill definition (read by Claude Code)
├── README.md                       # This file
├── scripts/
│   └── extract.py                  # Extraction script (stdlib only)
└── references/
    └── example_schemas.md          # Ready-made schemas for common doc types
```

## Example schemas

Pre-built schemas are included in [`references/example_schemas.md`](references/example_schemas.md) for:

- Invoices
- Receipts
- W-2 tax forms
- Bills of lading
- Purchase orders

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `KIE_API_URL` | KIE extraction API endpoint | `http://localhost:8000/v1/extract` |

## How it works

1. The document is base64-encoded and sent to the KIE API along with a JSON schema.
2. The API auto-detects document type (`pdf` vs `image`) by inspecting the file header.
3. The response contains extracted field values matching the schema keys.
4. Fields that could not be extracted are returned as `null`.

See the [root README](../README.md) for full API and schema format details.
