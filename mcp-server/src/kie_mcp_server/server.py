"""FastMCP server definition and tool registration."""

from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from kie_core import extract_document_async

server = FastMCP("kie-doc-extractor")


@server.tool()
async def extract_document(
    document_path: str,
    schema: dict,
    model: str | None = None,
) -> str:
    """Extract structured data from a document (image or PDF) using a JSON schema.

    Args:
        document_path: Path to the document file (PNG, JPG, TIFF, PDF, etc.).
        schema: JSON schema where keys are field names and values are type hints
                (e.g. "string", "number", "date (MM/DD/YYYY)").
        model: Optional model ID for extraction.

    Returns:
        Extracted field values as a JSON string.
    """
    result = await extract_document_async(document_path, schema, model=model)
    return json.dumps(result, indent=2, ensure_ascii=False)
