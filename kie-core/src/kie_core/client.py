"""KIE extraction API client (sync and async)."""

from __future__ import annotations

import os

import httpx

from kie_core.document import encode_document
from kie_core.schema import load_schema

DEFAULT_ENDPOINT = "http://localhost:8000/v1/extract"
DEFAULT_TIMEOUT = 120.0


def get_endpoint() -> str:
    """Return the KIE API endpoint from ``$KIE_API_URL`` or the default."""
    return os.environ.get("KIE_API_URL", DEFAULT_ENDPOINT)


# ── internal ──────────────────────────────────────────────────────────


def _build_payload(
    doc_base64: str,
    doc_type: str,
    schema: dict,
    model: str | None = None,
) -> dict:
    """Build the API request payload."""
    payload: dict = {
        "document": {"content": doc_base64, "type": doc_type},
        "schema": schema,
    }
    if model:
        payload["options"] = {"model": model}
    return payload


# ── low-level ─────────────────────────────────────────────────────────


def extract(
    doc_base64: str,
    doc_type: str,
    schema: dict,
    *,
    model: str | None = None,
    endpoint: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict:
    """Call the KIE extraction API (synchronous).

    Args:
        doc_base64: Base64-encoded document content.
        doc_type: Document type (``"pdf"`` or ``"image"``).
        schema: JSON schema defining the fields to extract.
        model: Optional model ID for extraction.
        endpoint: API endpoint URL.  Defaults to ``$KIE_API_URL`` or localhost.
        timeout: Request timeout in seconds.

    Returns:
        Extracted field values as a dict.

    Raises:
        RuntimeError: If the API request fails.
    """
    endpoint = endpoint or get_endpoint()
    payload = _build_payload(doc_base64, doc_type, schema, model)

    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        body = e.response.text
        raise RuntimeError(
            f"API request failed ({e.response.status_code}): {body}"
        ) from e
    except httpx.ConnectError as e:
        raise RuntimeError(f"Could not reach endpoint {endpoint}: {e}") from e
    except httpx.TimeoutException as e:
        raise RuntimeError(
            f"Request to {endpoint} timed out after {timeout}s"
        ) from e


async def extract_async(
    doc_base64: str,
    doc_type: str,
    schema: dict,
    *,
    model: str | None = None,
    endpoint: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict:
    """Call the KIE extraction API (asynchronous).

    Same parameters and semantics as :func:`extract`.
    """
    endpoint = endpoint or get_endpoint()
    payload = _build_payload(doc_base64, doc_type, schema, model)

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        body = e.response.text
        raise RuntimeError(
            f"API request failed ({e.response.status_code}): {body}"
        ) from e
    except httpx.ConnectError as e:
        raise RuntimeError(f"Could not reach endpoint {endpoint}: {e}") from e
    except httpx.TimeoutException as e:
        raise RuntimeError(
            f"Request to {endpoint} timed out after {timeout}s"
        ) from e


# ── high-level convenience ────────────────────────────────────────────


def extract_document(
    document_path: str,
    schema: dict | str,
    *,
    model: str | None = None,
    endpoint: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict:
    """Encode a document and extract fields in one call (sync).

    Args:
        document_path: Path to the document file.
        schema: JSON schema as a dict, JSON string, or path to a ``.json`` file.
        model: Optional model ID for extraction.
        endpoint: API endpoint URL.
        timeout: Request timeout in seconds.

    Returns:
        Extracted field values as a dict.
    """
    if isinstance(schema, str):
        schema = load_schema(schema)
    doc_base64, doc_type = encode_document(document_path)
    return extract(
        doc_base64, doc_type, schema, model=model, endpoint=endpoint, timeout=timeout
    )


async def extract_document_async(
    document_path: str,
    schema: dict | str,
    *,
    model: str | None = None,
    endpoint: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict:
    """Encode a document and extract fields in one call (async).

    Same parameters and semantics as :func:`extract_document`.
    """
    if isinstance(schema, str):
        schema = load_schema(schema)
    doc_base64, doc_type = encode_document(document_path)
    return await extract_async(
        doc_base64, doc_type, schema, model=model, endpoint=endpoint, timeout=timeout
    )
