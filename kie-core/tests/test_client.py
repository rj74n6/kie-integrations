"""Tests for kie_core.client — essential + comprehensive."""

import json
import os

import httpx
import pytest
import respx

from kie_core.client import (
    DEFAULT_ENDPOINT,
    _build_payload,
    extract,
    extract_async,
    extract_document,
    extract_document_async,
    get_endpoint,
)

MOCK_ENDPOINT = "http://testserver/v1/extract"


# ── essential ─────────────────────────────────────────────────────────


class TestExtractEssential:
    """Core sync client tests."""

    @respx.mock
    def test_success(self, mock_result):
        respx.post(MOCK_ENDPOINT).mock(
            return_value=httpx.Response(200, json=mock_result)
        )
        result = extract("b64data", "image", {"name": "string"}, endpoint=MOCK_ENDPOINT)
        assert result == mock_result

    @respx.mock
    def test_with_model(self):
        route = respx.post(MOCK_ENDPOINT).mock(
            return_value=httpx.Response(200, json={})
        )
        extract(
            "b64data", "pdf", {"x": "string"}, model="test-model", endpoint=MOCK_ENDPOINT
        )
        payload = json.loads(route.calls[0].request.content)
        assert payload["options"] == {"model": "test-model"}

    @respx.mock
    def test_without_model(self):
        route = respx.post(MOCK_ENDPOINT).mock(
            return_value=httpx.Response(200, json={})
        )
        extract("b64data", "image", {"x": "string"}, endpoint=MOCK_ENDPOINT)
        payload = json.loads(route.calls[0].request.content)
        assert "options" not in payload

    @respx.mock
    def test_http_error(self):
        respx.post(MOCK_ENDPOINT).mock(
            return_value=httpx.Response(400, text="Bad Request")
        )
        with pytest.raises(RuntimeError, match="API request failed.*400"):
            extract("b64", "image", {}, endpoint=MOCK_ENDPOINT)

    @respx.mock
    def test_connection_error(self):
        respx.post(MOCK_ENDPOINT).mock(side_effect=httpx.ConnectError("refused"))
        with pytest.raises(RuntimeError, match="Could not reach endpoint"):
            extract("b64", "image", {}, endpoint=MOCK_ENDPOINT)


class TestExtractAsyncEssential:
    """Core async client tests."""

    @respx.mock
    async def test_success(self, mock_result):
        respx.post(MOCK_ENDPOINT).mock(
            return_value=httpx.Response(200, json=mock_result)
        )
        result = await extract_async(
            "b64data", "image", {"name": "string"}, endpoint=MOCK_ENDPOINT
        )
        assert result == mock_result


# ── comprehensive ─────────────────────────────────────────────────────


class TestExtractComprehensive:
    """Payload structure, timeouts, and edge cases."""

    @respx.mock
    def test_payload_structure(self):
        route = respx.post(MOCK_ENDPOINT).mock(
            return_value=httpx.Response(200, json={})
        )
        extract(
            "dGVzdA==",
            "pdf",
            {"vendor": "string"},
            model="my-model",
            endpoint=MOCK_ENDPOINT,
        )
        payload = json.loads(route.calls[0].request.content)
        assert payload == {
            "document": {"content": "dGVzdA==", "type": "pdf"},
            "schema": {"vendor": "string"},
            "options": {"model": "my-model"},
        }

    @respx.mock
    def test_timeout(self):
        respx.post(MOCK_ENDPOINT).mock(side_effect=httpx.ReadTimeout("timeout"))
        with pytest.raises(RuntimeError, match="timed out"):
            extract("b64", "image", {}, endpoint=MOCK_ENDPOINT)

    @respx.mock
    def test_http_500(self):
        respx.post(MOCK_ENDPOINT).mock(
            return_value=httpx.Response(500, text="Internal Server Error")
        )
        with pytest.raises(RuntimeError, match="500"):
            extract("b64", "image", {}, endpoint=MOCK_ENDPOINT)

    @respx.mock
    def test_empty_response_body(self):
        respx.post(MOCK_ENDPOINT).mock(
            return_value=httpx.Response(200, json={})
        )
        result = extract("b64", "image", {"x": "string"}, endpoint=MOCK_ENDPOINT)
        assert result == {}


class TestExtractAsyncComprehensive:
    """Async edge cases."""

    @respx.mock
    async def test_http_error(self):
        respx.post(MOCK_ENDPOINT).mock(
            return_value=httpx.Response(502, text="Bad Gateway")
        )
        with pytest.raises(RuntimeError, match="502"):
            await extract_async("b64", "image", {}, endpoint=MOCK_ENDPOINT)

    @respx.mock
    async def test_timeout(self):
        respx.post(MOCK_ENDPOINT).mock(side_effect=httpx.ReadTimeout("timeout"))
        with pytest.raises(RuntimeError, match="timed out"):
            await extract_async("b64", "image", {}, endpoint=MOCK_ENDPOINT)

    @respx.mock
    async def test_with_model(self):
        route = respx.post(MOCK_ENDPOINT).mock(
            return_value=httpx.Response(200, json={})
        )
        await extract_async(
            "b64", "pdf", {"x": "string"}, model="m1", endpoint=MOCK_ENDPOINT
        )
        payload = json.loads(route.calls[0].request.content)
        assert payload["options"] == {"model": "m1"}


# ── high-level convenience ────────────────────────────────────────────


class TestExtractDocument:
    """Tests for the high-level extract_document / extract_document_async."""

    @respx.mock
    def test_sync_with_dict_schema(self, sample_image, mock_result):
        respx.post(MOCK_ENDPOINT).mock(
            return_value=httpx.Response(200, json=mock_result)
        )
        result = extract_document(
            str(sample_image), {"name": "string"}, endpoint=MOCK_ENDPOINT
        )
        assert result == mock_result

    @respx.mock
    def test_sync_with_string_schema(self, sample_image, mock_result):
        respx.post(MOCK_ENDPOINT).mock(
            return_value=httpx.Response(200, json=mock_result)
        )
        result = extract_document(
            str(sample_image), '{"name": "string"}', endpoint=MOCK_ENDPOINT
        )
        assert result == mock_result

    @respx.mock
    def test_sync_with_schema_file(self, sample_image, sample_schema_file, mock_result):
        respx.post(MOCK_ENDPOINT).mock(
            return_value=httpx.Response(200, json=mock_result)
        )
        result = extract_document(
            str(sample_image), str(sample_schema_file), endpoint=MOCK_ENDPOINT
        )
        assert result == mock_result

    @respx.mock
    async def test_async_with_dict_schema(self, sample_image, mock_result):
        respx.post(MOCK_ENDPOINT).mock(
            return_value=httpx.Response(200, json=mock_result)
        )
        result = await extract_document_async(
            str(sample_image), {"name": "string"}, endpoint=MOCK_ENDPOINT
        )
        assert result == mock_result

    def test_sync_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            extract_document("/no/such/file.png", {"x": "string"})


# ── get_endpoint ──────────────────────────────────────────────────────


class TestGetEndpoint:
    """Tests for endpoint resolution."""

    def test_default(self, monkeypatch):
        monkeypatch.delenv("KIE_API_URL", raising=False)
        assert get_endpoint() == DEFAULT_ENDPOINT

    def test_from_env(self, monkeypatch):
        monkeypatch.setenv("KIE_API_URL", "https://custom.example.com/extract")
        assert get_endpoint() == "https://custom.example.com/extract"


# ── _build_payload ────────────────────────────────────────────────────


class TestBuildPayload:
    """Tests for internal payload builder."""

    def test_without_model(self):
        p = _build_payload("b64", "image", {"x": "string"})
        assert "options" not in p

    def test_with_model(self):
        p = _build_payload("b64", "pdf", {"x": "string"}, model="m1")
        assert p["options"] == {"model": "m1"}
