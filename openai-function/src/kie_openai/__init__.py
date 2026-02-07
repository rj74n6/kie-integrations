"""OpenAI function-calling wrapper for KIE document extraction."""

from kie_openai.function_def import FUNCTION_DEF, TOOLS
from kie_openai.handler import handle_extract_document, handle_tool_call

__all__ = [
    "FUNCTION_DEF",
    "TOOLS",
    "handle_extract_document",
    "handle_tool_call",
]
