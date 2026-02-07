# KIE Document Extractor — OpenAI Function

An [OpenAI function calling](https://platform.openai.com/docs/guides/function-calling) definition and handler that lets GPT models invoke KIE document extraction as a tool.

## Installation

```bash
uv sync --package kie-openai
```

## Usage

### With the OpenAI SDK

```python
from openai import OpenAI
from kie_openai import TOOLS, handle_tool_call

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Extract the vendor and total from invoice.pdf"}],
    tools=TOOLS,
)

# Process tool calls
for tool_call in response.choices[0].message.tool_calls:
    result = handle_tool_call(tool_call)
    print(result)  # JSON string
```

### Direct handler usage

```python
from kie_openai import handle_extract_document

result = handle_extract_document(
    "invoice.pdf",
    {"vendor_name": "string", "total_amount": "number"},
)
```

## Exports

| Name | Description |
|------|-------------|
| `FUNCTION_DEF` | OpenAI function definition dict (single tool) |
| `TOOLS` | Ready-to-use `tools` list for `chat.completions.create(tools=...)` |
| `handle_extract_document(path, schema, model=None)` | Execute extraction, return JSON string |
| `handle_tool_call(tool_call)` | Dispatch an OpenAI tool call to the correct handler |

## Function definition

```json
{
  "type": "function",
  "function": {
    "name": "extract_document",
    "description": "Extract structured data from a document...",
    "parameters": {
      "type": "object",
      "properties": {
        "document_path": { "type": "string" },
        "schema": { "type": "object", "additionalProperties": true },
        "model": { "type": "string" }
      },
      "required": ["document_path", "schema"]
    }
  }
}
```

## File structure

```
openai-function/
├── README.md
├── pyproject.toml
├── src/
│   └── kie_openai/
│       ├── __init__.py
│       ├── function_def.py      # FUNCTION_DEF and TOOLS constants
│       └── handler.py           # Tool-call handler
└── tests/
    ├── conftest.py
    └── test_function.py
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `KIE_API_URL` | KIE extraction API endpoint | `http://localhost:8000/v1/extract` |

## Dependencies

- `kie-core` — shared extraction client (workspace dependency)

The `openai` SDK is **not** a dependency of this package — you bring your own. The handler only requires the tool-call object shape, not the SDK itself.

## Testing

```bash
uv run pytest openai-function/tests/ -v
```
