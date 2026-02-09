"""Shared fixtures for mcp-server tests."""

import base64

import pytest


@pytest.fixture()
def sample_b64():
    """Return a base64-encoded PNG-like payload and its document type."""
    raw = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
    return base64.b64encode(raw).decode("ascii"), "image"


@pytest.fixture()
def mock_result():
    """Return a typical extraction result."""
    return {"vendor_name": "Acme Corp", "total_amount": 1234.56}
