"""Shared fixtures for mcp-server tests."""

import json

import pytest


@pytest.fixture()
def sample_image(tmp_path):
    """Create a minimal PNG-like file."""
    img = tmp_path / "test.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
    return img


@pytest.fixture()
def mock_result():
    """Return a typical extraction result."""
    return {"vendor_name": "Acme Corp", "total_amount": 1234.56}
