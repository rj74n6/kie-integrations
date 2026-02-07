"""Tests for kie_openai — essential + comprehensive."""

import json
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from kie_openai import FUNCTION_DEF, TOOLS
from kie_openai.handler import handle_extract_document, handle_tool_call


def _make_tool_call(name: str, arguments: dict) -> SimpleNamespace:
    """Build a minimal tool-call object matching the OpenAI SDK shape."""
    return SimpleNamespace(
        function=SimpleNamespace(
            name=name,
            arguments=json.dumps(arguments),
        )
    )


# ── essential ─────────────────────────────────────────────────────────


class TestFunctionDefEssential:
    """Validate the function definition schema."""

    def test_structure(self):
        assert FUNCTION_DEF["type"] == "function"
        func = FUNCTION_DEF["function"]
        assert func["name"] == "extract_document"
        params = func["parameters"]
        assert "document_path" in params["properties"]
        assert "schema" in params["properties"]
        assert set(params["required"]) == {"document_path", "schema"}

    def test_tools_list(self):
        assert isinstance(TOOLS, list)
        assert len(TOOLS) == 1
        assert TOOLS[0] is FUNCTION_DEF


class TestHandlerEssential:
    """Core handler tests."""

    def test_handle_extract_document(self, sample_image, mock_result):
        with patch(
            "kie_openai.handler.extract_document", return_value=mock_result
        ):
            result = handle_extract_document(
                str(sample_image), {"vendor_name": "string"}
            )
        parsed = json.loads(result)
        assert parsed == mock_result

    def test_handle_tool_call(self, sample_image, mock_result):
        tc = _make_tool_call(
            "extract_document",
            {"document_path": str(sample_image), "schema": {"name": "string"}},
        )
        with patch(
            "kie_openai.handler.extract_document", return_value=mock_result
        ):
            result = handle_tool_call(tc)
        assert json.loads(result) == mock_result

    def test_unknown_function_raises(self):
        tc = _make_tool_call("unknown_fn", {})
        with pytest.raises(ValueError, match="Unknown function"):
            handle_tool_call(tc)


# ── comprehensive ─────────────────────────────────────────────────────


class TestFunctionDefComprehensive:
    """Extended schema validation."""

    def test_model_param_is_optional(self):
        params = FUNCTION_DEF["function"]["parameters"]
        assert "model" not in params["required"]

    def test_schema_allows_additional_properties(self):
        schema_prop = FUNCTION_DEF["function"]["parameters"]["properties"]["schema"]
        assert schema_prop.get("additionalProperties") is True

    def test_description_is_nonempty(self):
        assert len(FUNCTION_DEF["function"]["description"]) > 10


class TestHandlerComprehensive:
    """Extended handler tests."""

    def test_handler_returns_string(self, sample_image, mock_result):
        with patch(
            "kie_openai.handler.extract_document", return_value=mock_result
        ):
            result = handle_extract_document(
                str(sample_image), {"name": "string"}
            )
        assert isinstance(result, str)

    def test_handler_with_model(self, sample_image):
        with patch(
            "kie_openai.handler.extract_document", return_value={}
        ) as mock_fn:
            handle_extract_document(
                str(sample_image), {"x": "string"}, model="my-model"
            )
        mock_fn.assert_called_once_with(
            str(sample_image), {"x": "string"}, model="my-model"
        )

    def test_tool_call_with_model(self, sample_image):
        tc = _make_tool_call(
            "extract_document",
            {
                "document_path": str(sample_image),
                "schema": {"x": "string"},
                "model": "m1",
            },
        )
        with patch(
            "kie_openai.handler.extract_document", return_value={}
        ) as mock_fn:
            handle_tool_call(tc)
        mock_fn.assert_called_once_with(
            str(sample_image), {"x": "string"}, model="m1"
        )

    def test_unicode_result(self, sample_image):
        unicode_result = {"name": "日本語テスト", "amount": 100}
        with patch(
            "kie_openai.handler.extract_document", return_value=unicode_result
        ):
            result = handle_extract_document(
                str(sample_image), {"name": "string"}
            )
        parsed = json.loads(result)
        assert parsed["name"] == "日本語テスト"
