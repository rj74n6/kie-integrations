#!/usr/bin/env python3
"""
Extract structured data from a document using a JSON schema via MCP REST API.

Usage:
    python3 extract.py <document_path> <json_schema> [-o output.json] [--endpoint URL] [--model MODEL]

Arguments:
    document_path  Path to the document (PDF or image: PNG, JPG, TIFF, etc.)
    json_schema    JSON schema string or path to a .json schema file

Options:
    -o, --output    Path to save the extracted JSON result
    --endpoint      Extract API endpoint (default: $KIE_API_URL or http://localhost:8000/v1/extract)
    --model         Model ID to use for extraction (e.g., joy-vl-3b-sglang)

The script calls the KIE extraction API with the base64-encoded document
and JSON schema. Returns extracted field values as JSON to stdout.
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
from pathlib import Path


def load_schema(schema_input: str) -> dict:
    """Load schema from a JSON string or file path."""
    if os.path.isfile(schema_input):
        with open(schema_input) as f:
            return json.load(f)
    try:
        return json.loads(schema_input)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON schema: {e}")


def encode_document(document_path: str) -> tuple[str, str]:
    """Read and base64-encode a document. Returns (base64_data, doc_type)."""
    path = Path(document_path)
    if not path.exists():
        raise FileNotFoundError(f"Document not found: {document_path}")

    doc_bytes = path.read_bytes()
    doc_base64 = base64.b64encode(doc_bytes).decode("ascii")
    doc_type = "pdf" if doc_bytes.startswith(b"%PDF") else "image"

    return doc_base64, doc_type


def call_extract_api(endpoint: str, doc_base64: str, doc_type: str, schema: dict, model: str | None = None) -> dict:
    """Call the MCP extraction REST API."""
    payload = {
        "document": {"content": doc_base64, "type": doc_type},
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
        with urllib.request.urlopen(req, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        raise RuntimeError(f"API request failed ({e.code}): {error_body}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Could not reach endpoint {endpoint}: {e.reason}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract structured data from a document via MCP extraction API."
    )
    parser.add_argument("document_path", help="Path to the document (PDF or image)")
    parser.add_argument("schema", help="JSON schema string or path to .json file")
    parser.add_argument("-o", "--output", help="Path to save the result JSON")
    parser.add_argument(
        "--endpoint",
        default=os.environ.get("KIE_API_URL", "http://localhost:8000/v1/extract"),
        help="Extract API endpoint (default: $KIE_API_URL or http://localhost:8000/v1/extract)",
    )
    parser.add_argument("--model", help="Model ID for extraction (e.g., joy-vl-3b-sglang)")

    args = parser.parse_args()

    # Load inputs
    schema = load_schema(args.schema)
    doc_base64, doc_type = encode_document(args.document_path)

    # Call extraction API
    result = call_extract_api(args.endpoint, doc_base64, doc_type, schema, args.model)

    # Output
    result_json = json.dumps(result, indent=2, ensure_ascii=False)
    print(result_json)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w") as f:
            f.write(result_json)
        print(f"\nSaved to: {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
