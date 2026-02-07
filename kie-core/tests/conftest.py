"""Shared fixtures for kie-core tests."""

import json

import pytest


@pytest.fixture()
def sample_image(tmp_path):
    """Create a minimal PNG-like file."""
    img = tmp_path / "test.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
    return img


@pytest.fixture()
def sample_pdf(tmp_path):
    """Create a minimal PDF-like file."""
    pdf = tmp_path / "test.pdf"
    pdf.write_bytes(b"%PDF-1.4 test content")
    return pdf


@pytest.fixture()
def sample_schema():
    """Return a simple extraction schema."""
    return {"vendor_name": "string", "total_amount": "number"}


@pytest.fixture()
def sample_schema_file(tmp_path, sample_schema):
    """Write a schema to a temporary JSON file."""
    path = tmp_path / "schema.json"
    path.write_text(json.dumps(sample_schema))
    return path


@pytest.fixture()
def mock_endpoint():
    """Return a deterministic test endpoint URL."""
    return "http://testserver/v1/extract"


@pytest.fixture()
def mock_result():
    """Return a typical extraction result."""
    return {"vendor_name": "Acme Corp", "total_amount": 1234.56}
