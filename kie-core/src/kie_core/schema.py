"""JSON schema loading utilities."""

import json
import os


def load_schema(schema_input: str | dict) -> dict:
    """Load a schema from a JSON string, file path, or dict.

    Args:
        schema_input: JSON string, path to a .json file, or dict.

    Returns:
        Parsed schema as a dict.

    Raises:
        ValueError: If the input is not valid JSON.
    """
    if isinstance(schema_input, dict):
        return schema_input

    if os.path.isfile(schema_input):
        with open(schema_input) as f:
            return json.load(f)

    try:
        return json.loads(schema_input)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON schema: {e}") from e
