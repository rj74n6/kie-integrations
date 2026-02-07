"""Tests for kie_core.document — essential + comprehensive."""

import base64

import pytest

from kie_core.document import encode_document


# ── essential ─────────────────────────────────────────────────────────


class TestEncodeDocumentEssential:
    """Core encoding tests."""

    def test_encode_image(self, sample_image):
        b64, doc_type = encode_document(sample_image)
        assert doc_type == "image"
        assert base64.b64decode(b64)  # valid base64

    def test_encode_pdf(self, sample_pdf):
        b64, doc_type = encode_document(sample_pdf)
        assert doc_type == "pdf"
        assert base64.b64decode(b64)

    def test_not_found_raises(self):
        with pytest.raises(FileNotFoundError, match="Document not found"):
            encode_document("/nonexistent/file.png")

    def test_round_trip(self, sample_image):
        original = sample_image.read_bytes()
        b64, _ = encode_document(sample_image)
        assert base64.b64decode(b64) == original


# ── comprehensive ─────────────────────────────────────────────────────


class TestEncodeDocumentComprehensive:
    """Format detection and edge cases."""

    @pytest.mark.parametrize(
        "ext, magic, expected_type",
        [
            ("png", b"\x89PNG\r\n\x1a\n", "image"),
            ("jpg", b"\xff\xd8\xff\xe0", "image"),
            ("tiff_le", b"II*\x00", "image"),
            ("tiff_be", b"MM\x00*", "image"),
            ("bmp", b"BM\x00\x00", "image"),
            ("webp", b"RIFF\x00\x00\x00\x00WEBP", "image"),
            ("pdf14", b"%PDF-1.4", "pdf"),
            ("pdf20", b"%PDF-2.0", "pdf"),
        ],
    )
    def test_various_formats(self, tmp_path, ext, magic, expected_type):
        doc = tmp_path / f"test.{ext}"
        doc.write_bytes(magic + b"\x00" * 50)
        _, doc_type = encode_document(doc)
        assert doc_type == expected_type

    def test_string_path(self, sample_image):
        """Accepts a plain string path, not just Path objects."""
        b64, doc_type = encode_document(str(sample_image))
        assert doc_type == "image"
        assert b64

    def test_empty_file(self, tmp_path):
        """An empty file is detected as image (not PDF)."""
        f = tmp_path / "empty"
        f.write_bytes(b"")
        b64, doc_type = encode_document(f)
        assert doc_type == "image"
        assert b64 == ""

    def test_large_ish_file(self, tmp_path):
        """Encode a ~1 MB file without issues."""
        f = tmp_path / "big.png"
        f.write_bytes(b"\x89PNG" + b"\xab" * (1024 * 1024))
        b64, doc_type = encode_document(f)
        assert doc_type == "image"
        assert len(b64) > 1_000_000
