"""Tests for kie_mcp_server — essential + comprehensive."""

import json
from unittest.mock import AsyncMock, patch

import pytest

from kie_mcp_server.server import extract_document, server


# ── essential ─────────────────────────────────────────────────────────


class TestMCPServerEssential:
    """Core tool registration and invocation tests."""

    def test_server_name(self):
        assert server.name == "kie-doc-extractor"

    async def test_tool_is_registered(self):
        """The server exposes at least the extract_document tool."""
        tools = await server.list_tools()
        names = [t.name for t in tools]
        assert "extract_document" in names

    async def test_tool_schema_has_required_params(self):
        tools = await server.list_tools()
        tool = next(t for t in tools if t.name == "extract_document")
        props = tool.inputSchema.get("properties", {})
        assert "document_path" in props
        assert "schema" in props

    async def test_extract_tool_call(self, sample_image, mock_result):
        with patch(
            "kie_mcp_server.server.extract_document_async",
            new_callable=AsyncMock,
            return_value=mock_result,
        ):
            result_str = await extract_document(
                str(sample_image), {"vendor_name": "string"}
            )
        parsed = json.loads(result_str)
        assert parsed == mock_result


# ── comprehensive ─────────────────────────────────────────────────────


class TestMCPServerComprehensive:
    """Extended tests."""

    async def test_extract_with_model(self, sample_image, mock_result):
        with patch(
            "kie_mcp_server.server.extract_document_async",
            new_callable=AsyncMock,
            return_value=mock_result,
        ) as mock_fn:
            await extract_document(
                str(sample_image), {"name": "string"}, model="test-model"
            )
        mock_fn.assert_awaited_once_with(
            str(sample_image), {"name": "string"}, model="test-model"
        )

    async def test_extract_returns_json_string(self, sample_image):
        with patch(
            "kie_mcp_server.server.extract_document_async",
            new_callable=AsyncMock,
            return_value={"a": 1},
        ):
            result = await extract_document(str(sample_image), {"a": "number"})
        # Must be valid JSON string
        assert isinstance(result, str)
        assert json.loads(result) == {"a": 1}

    async def test_extract_api_error_propagates(self, sample_image):
        with patch(
            "kie_mcp_server.server.extract_document_async",
            new_callable=AsyncMock,
            side_effect=RuntimeError("API request failed (500): error"),
        ):
            with pytest.raises(RuntimeError, match="API request failed"):
                await extract_document(str(sample_image), {"x": "string"})

    async def test_tool_schema_model_is_optional(self):
        tools = await server.list_tools()
        tool = next(t for t in tools if t.name == "extract_document")
        required = tool.inputSchema.get("required", [])
        assert "model" not in required

    async def test_concurrent_calls(self, sample_image, mock_result):
        """Two concurrent calls don't interfere."""
        import asyncio

        with patch(
            "kie_mcp_server.server.extract_document_async",
            new_callable=AsyncMock,
            return_value=mock_result,
        ):
            r1, r2 = await asyncio.gather(
                extract_document(str(sample_image), {"a": "string"}),
                extract_document(str(sample_image), {"b": "number"}),
            )
        assert json.loads(r1) == mock_result
        assert json.loads(r2) == mock_result
