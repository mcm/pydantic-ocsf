"""Utility functions for code generation."""

from __future__ import annotations

import re


def snake_to_pascal(name: str) -> str:
    """Convert snake_case to PascalCase.

    Examples:
        file_activity -> FileActivity
        dns_activity -> DnsActivity (not DNSActivity)
        http_activity -> HttpActivity (not HTTPActivity)
    """
    return "".join(word.capitalize() for word in name.split("_"))


def ocsf_type_to_python(
    ocsf_type: str,
    is_array: bool = False,
    object_type: str | None = None,
    enum_name: str | None = None,
) -> str:
    """Convert OCSF type to Python type annotation.

    Args:
        ocsf_type: OCSF type string (e.g., "string_t", "integer_t")
        is_array: Whether the field is an array
        object_type: For object_t, the referenced object name
        enum_name: If this field has an associated enum

    Returns:
        Python type annotation string
    """
    # Handle enum types
    if enum_name:
        python_type = snake_to_pascal(enum_name)
    # Handle object references
    elif ocsf_type == "object_t" and object_type:
        python_type = snake_to_pascal(object_type)
    # Map primitive types
    else:
        type_map = {
            "string_t": "str",
            "integer_t": "int",
            "long_t": "int",
            "float_t": "float",
            "boolean_t": "bool",
            "timestamp_t": "int",
            "datetime_t": "str",
            "json_t": "dict[str, Any]",
            "object_t": "dict[str, Any]",  # Fallback if no object_type
        }
        python_type = type_map.get(ocsf_type, "Any")

    # Wrap in list if array
    if is_array:
        return f"list[{python_type}]"

    return python_type


def make_valid_identifier(name: str) -> str:
    """Ensure a string is a valid Python identifier.

    Handles reserved words and invalid characters.
    """
    # Python reserved words
    reserved = {
        "False",
        "None",
        "True",
        "and",
        "as",
        "assert",
        "async",
        "await",
        "break",
        "class",
        "continue",
        "def",
        "del",
        "elif",
        "else",
        "except",
        "finally",
        "for",
        "from",
        "global",
        "if",
        "import",
        "in",
        "is",
        "lambda",
        "nonlocal",
        "not",
        "or",
        "pass",
        "raise",
        "return",
        "try",
        "while",
        "with",
        "yield",
        "type",
    }

    # Remove invalid characters first (this may introduce leading underscores)
    name = re.sub(r"[^a-zA-Z0-9_]", "_", name)

    # Pydantic doesn't allow field names starting with underscore
    # Strip leading underscores
    if name.startswith("_"):
        name = name.lstrip("_")
        if not name:  # If name was all underscores
            name = "field"

    # Ensure doesn't start with number
    if name and name[0].isdigit():
        name = f"field_{name}"

    if name in reserved:
        return f"{name}_"

    return name


def format_docstring(text: str, indent: int = 4) -> str:
    """Format a description as a Python docstring.

    Args:
        text: Raw description text
        indent: Number of spaces for indentation

    Returns:
        Formatted docstring content (without triple quotes)
    """
    if not text:
        return ""

    # Clean up whitespace
    text = text.strip()
    text = re.sub(r"\s+", " ", text)

    # Wrap long lines (accounting for indent and docstring margins)
    max_width = 100 - indent - 4
    words = text.split()
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 > max_width and current_line:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += len(word) + 1

    if current_line:
        lines.append(" ".join(current_line))

    return "\n".join(lines)
