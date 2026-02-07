"""OpenAI function definition for KIE document extraction."""

FUNCTION_DEF: dict = {
    "type": "function",
    "function": {
        "name": "extract_document",
        "description": (
            "Extract structured data from a document (image or PDF) "
            "using a JSON schema. Returns extracted field values as JSON."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "document_path": {
                    "type": "string",
                    "description": "Path to the document file (PNG, JPG, TIFF, PDF, etc.)",
                },
                "schema": {
                    "type": "object",
                    "description": (
                        "JSON schema where keys are field names and values are type hints "
                        '(e.g. "string", "number", "date (MM/DD/YYYY)")'
                    ),
                    "additionalProperties": True,
                },
                "model": {
                    "type": "string",
                    "description": "Optional model ID for extraction (e.g. 'joy-vl-3b-sglang')",
                },
            },
            "required": ["document_path", "schema"],
        },
    },
}

TOOLS: list[dict] = [FUNCTION_DEF]
"""Ready-to-use ``tools`` list for ``client.chat.completions.create(tools=TOOLS)``."""
