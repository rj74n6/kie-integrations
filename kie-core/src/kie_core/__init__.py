"""Core client library for the KIE document extraction API."""

from kie_core.client import (
    extract,
    extract_async,
    extract_document,
    extract_document_async,
    get_endpoint,
)
from kie_core.document import encode_document
from kie_core.schema import load_schema

__all__ = [
    "encode_document",
    "extract",
    "extract_async",
    "extract_document",
    "extract_document_async",
    "get_endpoint",
    "load_schema",
]
