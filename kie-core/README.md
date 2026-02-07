# kie-core

Core client library for the KIE document extraction API. Provides sync and async Python functions used by all integration packages.

## Installation

```bash
uv add kie-core
```

Or as a workspace dependency (used by sibling packages in this repo):

```toml
[project]
dependencies = ["kie-core"]

[tool.uv.sources]
kie-core = { workspace = true }
```

## Usage

### High-level (recommended)

```python
from kie_core import extract_document

result = extract_document(
    "invoice.pdf",
    {"vendor_name": "string", "total_amount": "number"},
)
print(result)
# {"vendor_name": "Acme Corp", "total_amount": 1234.56}
```

Async variant:

```python
from kie_core import extract_document_async

result = await extract_document_async(
    "invoice.pdf",
    {"vendor_name": "string", "total_amount": "number"},
)
```

The schema can be a `dict`, a JSON string, or a path to a `.json` file.

### Low-level

```python
from kie_core import encode_document, extract, load_schema

schema = load_schema('{"vendor_name": "string"}')
doc_base64, doc_type = encode_document("invoice.pdf")
result = extract(doc_base64, doc_type, schema, model="joy-vl-3b-sglang")
```

## API reference

| Function | Description |
|----------|-------------|
| `load_schema(input)` | Parse a schema from a dict, JSON string, or file path |
| `encode_document(path)` | Base64-encode a document; returns `(base64, "pdf"\|"image")` |
| `extract(b64, type, schema, ...)` | Call the KIE API (sync) |
| `extract_async(b64, type, schema, ...)` | Call the KIE API (async) |
| `extract_document(path, schema, ...)` | Encode + extract in one call (sync) |
| `extract_document_async(path, schema, ...)` | Encode + extract in one call (async) |
| `get_endpoint()` | Resolve API URL from `$KIE_API_URL` or default |

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `KIE_API_URL` | KIE extraction API endpoint | `http://localhost:8000/v1/extract` |

## Dependencies

- `httpx` — HTTP client (sync + async)

Python 3.10+ required.

## Testing

```bash
uv run pytest kie-core/tests/ -v
```
