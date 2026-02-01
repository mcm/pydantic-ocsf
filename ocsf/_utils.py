"""Utility functions for OCSF model creation."""

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


def pascal_to_snake(name: str) -> str:
    """Convert PascalCase to snake_case.

    Args:
        name: PascalCase name (e.g., "User", "FileActivity", "Finding")

    Returns:
        snake_case name (e.g., "user", "file_activity", "finding")

    Examples:
        FileActivity -> file_activity
        APIKey -> api_key
        Finding -> finding
    """
    # Insert underscores before uppercase letters that follow lowercase letters
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    # Insert underscores before uppercase letters that follow lowercase or uppercase letters
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
    return s2.lower()


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


def label_to_enum_name(label: str) -> str:
    """Convert an enum label to a valid Python enum member name.

    Args:
        label: Enum label from OCSF schema (e.g., "Create", "Does not exist")

    Returns:
        Valid Python enum member name in UPPER_SNAKE_CASE

    Examples:
        "Create" -> "CREATE"
        "Does not exist" -> "DOES_NOT_EXIST"
        "Cat I" -> "CAT_I"
        "Unknown" -> "UNKNOWN"
        "Other" -> "OTHER"
    """
    # Replace spaces and hyphens with underscores
    name = re.sub(r"[\s\-]+", "_", label)
    # Remove any other special characters
    name = re.sub(r"[^a-zA-Z0-9_]", "", name)
    # Convert to uppercase
    name = name.upper()
    # Remove leading/trailing underscores
    name = name.strip("_")
    # Collapse multiple underscores
    name = re.sub(r"_+", "_", name)

    # Ensure doesn't start with a number
    if name and name[0].isdigit():
        name = f"VALUE_{name}"

    # Fallback for empty or invalid names
    if not name:
        name = "UNKNOWN"

    return name
