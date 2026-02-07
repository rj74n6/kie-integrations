#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp>=1.0"]
# ///
"""
MCP server for KIE document extraction.

Exposes an `extract_document` tool that extracts structured data from
documents (images/PDFs) using a JSON schema.  Self-contained — only
requires the `mcp` package (installed automatically by `uv run`).

Start with:
    uv run scripts/mcp-server.py
"""

from __future__ import annotations

import base64
import json
import os
import urllib.request
from pathlib import Path

from mcp.server.fastmcp import FastMCP

server = FastMCP("doc-extractor")

DEFAULT_ENDPOINT = "http://localhost:8000/v1/extract"


# ── extraction helpers (stdlib only, no external deps) ────────────────


def _get_endpoint() -> str:
    return os.environ.get("KIE_API_URL", DEFAULT_ENDPOINT)


def _encode_document(document_path: str) -> tuple[str, str]:
    path = Path(document_path)
    if not path.exists():
        raise FileNotFoundError(f"Document not found: {document_path}")
    doc_bytes = path.read_bytes()
    b64 = base64.b64encode(doc_bytes).decode("ascii")
    doc_type = "pdf" if doc_bytes.startswith(b"%PDF") else "image"
    return b64, doc_type


def _call_api(
    doc_b64: str,
    doc_type: str,
    schema: dict,
    model: str | None = None,
) -> dict:
    endpoint = _get_endpoint()
    payload: dict = {
        "document": {"content": doc_b64, "type": doc_type},
        "schema": schema,
    }
    if model:
        payload["options"] = {"model": model}

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        raise RuntimeError(f"API request failed ({e.code}): {body}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Could not reach endpoint {endpoint}: {e.reason}")


# ── MCP tool ──────────────────────────────────────────────────────────


@server.tool()
def extract_document(
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
    b64, doc_type = _encode_document(document_path)
    result = _call_api(b64, doc_type, schema, model)
    return json.dumps(result, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    server.run()
