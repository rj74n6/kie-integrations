"""Tests for kie_core.schema — essential + comprehensive."""

import json

import pytest

from kie_core.schema import load_schema


# ── essential ─────────────────────────────────────────────────────────


class TestLoadSchemaEssential:
    """Core happy-path and error-path tests."""

    def test_load_from_string(self, sample_schema):
        result = load_schema(json.dumps(sample_schema))
        assert result == sample_schema

    def test_load_from_file(self, sample_schema_file, sample_schema):
        result = load_schema(str(sample_schema_file))
        assert result == sample_schema

    def test_load_from_dict(self, sample_schema):
        result = load_schema(sample_schema)
        assert result is sample_schema

    def test_invalid_json_raises(self):
        with pytest.raises(ValueError, match="Invalid JSON schema"):
            load_schema("{bad json")


# ── comprehensive ─────────────────────────────────────────────────────


class TestLoadSchemaComprehensive:
    """Edge cases and extra coverage."""

    def test_empty_object_string(self):
        assert load_schema("{}") == {}

    def test_nested_schema(self):
        schema = {
            "line_items": [
                {"description": "string", "qty": "number", "price": "number"}
            ]
        }
        assert load_schema(json.dumps(schema)) == schema

    def test_nonexistent_path_treated_as_json(self):
        """A path-like string that doesn't exist is parsed as JSON (and fails)."""
        with pytest.raises(ValueError, match="Invalid JSON schema"):
            load_schema("/no/such/file.json")

    def test_file_with_nested_content(self, tmp_path):
        schema = {"items": [{"a": "string"}], "total": "number"}
        path = tmp_path / "nested.json"
        path.write_text(json.dumps(schema))
        assert load_schema(str(path)) == schema

    def test_unicode_values(self):
        schema = {"名前": "string", "金額": "number"}
        assert load_schema(json.dumps(schema)) == schema
