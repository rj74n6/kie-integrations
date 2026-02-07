"""Tool-call handler for OpenAI function calling."""

from __future__ import annotations

import json
from typing import Any

from kie_core import extract_document


def handle_extract_document(
    document_path: str,
    schema: dict,
    model: str | None = None,
) -> str:
    """Execute a ``extract_document`` tool call and return a JSON string.

    Args:
        document_path: Path to the document file.
        schema: JSON schema defining the fields to extract.
        model: Optional model ID for extraction.

    Returns:
        JSON-serialised extraction result (string), suitable for an OpenAI
        tool-response message.
    """
    result = extract_document(document_path, schema, model=model)
    return json.dumps(result, ensure_ascii=False)


def handle_tool_call(tool_call: Any) -> str:
    """Dispatch an OpenAI tool call to the correct handler.

    Args:
        tool_call: An ``openai.types.chat.ChatCompletionMessageToolCall``
                   (or any object with ``.function.name`` and ``.function.arguments``).

    Returns:
        JSON string result.

    Raises:
        ValueError: If the function name is not recognised.
    """
    name = tool_call.function.name
    args: dict = json.loads(tool_call.function.arguments)

    if name == "extract_document":
        return handle_extract_document(**args)

    raise ValueError(f"Unknown function: {name}")
