"""Tests for kie_langchain — essential + comprehensive."""

from unittest.mock import AsyncMock, patch

import pytest

from kie_langchain import KIEExtractDocumentTool


# ── essential ─────────────────────────────────────────────────────────


class TestToolEssential:
    """Core tool metadata and invocation tests."""

    def test_tool_metadata(self):
        tool = KIEExtractDocumentTool()
        assert tool.name == "extract_document"
        assert "document" in tool.description.lower()
        assert tool.args_schema is not None

    def test_invoke_sync(self, sample_image, mock_result):
        tool = KIEExtractDocumentTool()
        with patch(
            "kie_langchain.tool.extract_document", return_value=mock_result
        ):
            result = tool._run(str(sample_image), {"vendor_name": "string"})
        assert result == mock_result

    async def test_invoke_async(self, sample_image, mock_result):
        tool = KIEExtractDocumentTool()
        with patch(
            "kie_langchain.tool.extract_document_async",
            new_callable=AsyncMock,
            return_value=mock_result,
        ):
            result = await tool._arun(str(sample_image), {"vendor_name": "string"})
        assert result == mock_result

    def test_pydantic_input_schema(self):
        tool = KIEExtractDocumentTool()
        schema = tool.args_schema.model_json_schema()
        props = schema["properties"]
        assert "document_path" in props
        assert "schema" in props


# ── comprehensive ─────────────────────────────────────────────────────


class TestToolComprehensive:
    """Extended tool tests."""

    def test_tool_description_is_informative(self):
        tool = KIEExtractDocumentTool()
        assert "extract" in tool.description.lower()
        assert "json" in tool.description.lower()

    def test_invoke_with_model(self, sample_image):
        tool = KIEExtractDocumentTool()
        with patch(
            "kie_langchain.tool.extract_document", return_value={}
        ) as mock_fn:
            tool._run(str(sample_image), {"x": "string"}, model="my-model")
        mock_fn.assert_called_once_with(
            str(sample_image), {"x": "string"}, model="my-model"
        )

    async def test_ainvoke_with_model(self, sample_image):
        tool = KIEExtractDocumentTool()
        with patch(
            "kie_langchain.tool.extract_document_async",
            new_callable=AsyncMock,
            return_value={},
        ) as mock_fn:
            await tool._arun(str(sample_image), {"x": "string"}, model="m1")
        mock_fn.assert_awaited_once_with(
            str(sample_image), {"x": "string"}, model="m1"
        )

    def test_error_propagation(self, sample_image):
        tool = KIEExtractDocumentTool()
        with patch(
            "kie_langchain.tool.extract_document",
            side_effect=RuntimeError("API request failed (500): error"),
        ):
            with pytest.raises(RuntimeError, match="API request failed"):
                tool._run(str(sample_image), {"x": "string"})

    async def test_async_error_propagation(self, sample_image):
        tool = KIEExtractDocumentTool()
        with patch(
            "kie_langchain.tool.extract_document_async",
            new_callable=AsyncMock,
            side_effect=RuntimeError("API request failed (500): error"),
        ):
            with pytest.raises(RuntimeError, match="API request failed"):
                await tool._arun(str(sample_image), {"x": "string"})

    def test_model_field_is_optional_in_schema(self):
        tool = KIEExtractDocumentTool()
        schema = tool.args_schema.model_json_schema()
        required = schema.get("required", [])
        assert "model" not in required

    def test_returns_dict(self, sample_image, mock_result):
        tool = KIEExtractDocumentTool()
        with patch(
            "kie_langchain.tool.extract_document", return_value=mock_result
        ):
            result = tool._run(str(sample_image), {"x": "string"})
        assert isinstance(result, dict)
