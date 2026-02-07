"""KIE document extraction as a LangChain tool."""

from __future__ import annotations

import warnings
from typing import Any, Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from kie_core import extract_document, extract_document_async

# Pydantic warns that "schema" shadows BaseModel.schema(); this is intentional
# because "schema" is the natural parameter name for LLM-facing tool input.
warnings.filterwarnings("ignore", message='Field name "schema" in')


class ExtractDocumentInput(BaseModel):
    """Input schema for the KIE extraction tool."""

    model_config = {"protected_namespaces": ()}

    document_path: str = Field(
        description="Path to the document file (PNG, JPG, TIFF, PDF, etc.)"
    )
    schema: dict = Field(  # noqa: A003
        description=(
            "JSON schema where keys are field names and values are type hints "
            '(e.g. "string", "number", "date (MM/DD/YYYY)")'
        ),
    )
    model: str | None = Field(
        default=None,
        description="Optional model ID for extraction",
    )


class KIEExtractDocumentTool(BaseTool):
    """LangChain tool that extracts structured data from documents via the KIE API."""

    name: str = "extract_document"
    description: str = (
        "Extract structured data from a document (image or PDF) "
        "using a JSON schema. Returns extracted field values as JSON."
    )
    args_schema: Type[BaseModel] = ExtractDocumentInput

    def _run(
        self,
        document_path: str,
        schema: dict,
        model: str | None = None,
        **kwargs: Any,
    ) -> dict:
        """Execute extraction synchronously."""
        return extract_document(document_path, schema, model=model)

    async def _arun(
        self,
        document_path: str,
        schema: dict,
        model: str | None = None,
        **kwargs: Any,
    ) -> dict:
        """Execute extraction asynchronously."""
        return await extract_document_async(document_path, schema, model=model)
