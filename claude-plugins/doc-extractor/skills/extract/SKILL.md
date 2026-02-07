---
name: extract
description: Extract structured data from document images or PDFs using a JSON schema. Calls a KIE extraction API and returns field values as JSON.
---

# Document Extractor

Extract structured field values from documents (images or PDFs) by calling a KIE extraction API with a user-provided JSON schema.

## Workflow

1. **Collect inputs** — Obtain from the user:
   - A document file (PNG, JPG, TIFF, PDF, etc.)
   - A JSON schema defining the fields to extract

   If the user provides only a document without a schema, ask what fields they want extracted, then construct the schema. See `<skill_dir>/references/example_schemas.md` for common templates.

2. **Run extraction** — Execute the script:
   ```bash
   python3 <skill_dir>/scripts/extract.py "<document_path>" '<json_schema>' -o <output_path>
   ```
   Options:
   - `--endpoint <URL>` — Override the API endpoint (default: `$KIE_API_URL` or `http://localhost:8000/v1/extract`)
   - `--model <ID>` — Specify a model (e.g., `joy-vl-3b-sglang`)

   The schema can be passed as an inline JSON string or a path to a `.json` file.

3. **Review and return** — Check the output JSON for completeness. If any fields are `null`, note this to the user. Return the result.

## API Details

The script POSTs to the KIE extraction endpoint with this payload:
```json
{
  "document": {"content": "<base64>", "type": "pdf|image"},
  "schema": { ... },
  "options": {"model": "<model_id>"}
}
```

The document type is auto-detected: files starting with `%PDF` are sent as `"pdf"`, everything else as `"image"`. The `options.model` field is only included when `--model` is specified.

## Schema Format

Keys are field names; values describe expected types:

```json
{
  "vendor_name": "string",
  "invoice_date": "date (MM/DD/YYYY)",
  "total_amount": "number",
  "line_items": [{"description": "string", "qty": "number", "price": "number"}]
}
```

Supported hints: `"string"`, `"number"`, `"date (FORMAT)"`, `"boolean"`, `"currency"`, arrays of objects for tables/line items, or any descriptive hint like `"5-digit zip code"`.

## Configuration

Set the `KIE_API_URL` environment variable to point to your extraction service. Defaults to `http://localhost:8000/v1/extract`.
