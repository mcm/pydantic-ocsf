"""Utility functions for OCSF model creation."""

from __future__ import annotations

import re
from typing import Any


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


def infer_sibling_label_field(id_field: str) -> str:
    """Infer the sibling label field name for an ID field with an enum.

    Per OCSF specification, sibling attributes follow the pattern where a
    numeric `_id` field (e.g., activity_id, type_id) has a corresponding
    string label field. The label field name is inferred by removing the
    `_id` suffix, with special handling for Python reserved keywords.

    Args:
        id_field: The ID field name ending in "_id" (e.g., "activity_id", "type_id")

    Returns:
        The inferred label field name (e.g., "activity", "type_")

    Raises:
        ValueError: If field name doesn't end with "_id"

    Examples:
        >>> infer_sibling_label_field("activity_id")
        "activity"
        >>> infer_sibling_label_field("type_id")
        "type_"
        >>> infer_sibling_label_field("severity_id")
        "severity"
        >>> infer_sibling_label_field("class_id")
        "class_"

    Note:
        For Python reserved keywords (type, class, import, etc.), an underscore
        suffix is appended to avoid syntax errors.
    """
    if not id_field.endswith("_id"):
        raise ValueError(f"Expected field ending in '_id', got {id_field!r}")

    # Remove "_id" suffix to get base name
    base = id_field[:-3]

    # Python reserved keywords that need underscore suffix
    # This is a comprehensive list of Python 3.x keywords
    RESERVED_KEYWORDS = {
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

    # Check if base name is a reserved keyword (case-insensitive check)
    if base in RESERVED_KEYWORDS or base.lower() in {k.lower() for k in RESERVED_KEYWORDS}:
        return f"{base}_"

    return base


def extract_observable_type_ids(schema: dict[str, Any]) -> dict[int, str]:
    """Extract all observable type_id values from the schema.

    Observable.TypeId is a derived enum - its values are collected from all
    places in the schema where the "observable" field is defined. This function
    scans the entire schema to collect these definitions.

    Per OCSF specification, observables can be defined in 6 ways:
    1. Observable by dictionary type (e.g., email_t)
    2. Observable by dictionary attribute (e.g., cmd_line)
    3. Observable by object (e.g., container)
    4. Observable by event class attribute
    5. Observable by object attribute (e.g., cve.uid)
    6. Observable by class-specific attribute path

    Args:
        schema: Parsed OCSF schema dictionary

    Returns:
        Dictionary mapping observable type_id (int) to caption (str)
        Includes the standard 0 (Unknown) and 99 (Other) values

    Example:
        {
            0: "Unknown",
            1: "Hostname",
            2: "IP Address",
            5: "Email Address",
            ...
            99: "Other"
        }
    """
    observable_types: dict[int, str] = {}

    # Always include standard values
    observable_types[0] = "Unknown"
    observable_types[99] = "Other"

    # 1. Scan dictionary types for observable definitions
    dictionary = schema.get("dictionary", {})
    dict_types = dictionary.get("types", {})
    if dict_types and isinstance(dict_types, dict):
        type_attrs = dict_types.get("attributes", {})
        if type_attrs:
            for type_name, type_def in type_attrs.items():
                if isinstance(type_def, dict) and "observable" in type_def:
                    obs_id = type_def["observable"]
                    if isinstance(obs_id, int):
                        # Use the caption as the label
                        caption = type_def.get("caption", snake_to_pascal(type_name))
                        observable_types[obs_id] = caption

    # 2. Scan dictionary attributes for observable definitions
    dict_attributes = dictionary.get("attributes", {})
    for attr_name, attr_def in dict_attributes.items():
        if isinstance(attr_def, dict) and "observable" in attr_def:
            obs_id = attr_def["observable"]
            if isinstance(obs_id, int):
                caption = attr_def.get("caption", snake_to_pascal(attr_name))
                observable_types[obs_id] = caption

    # 3. Scan objects for top-level observable definitions (observable by object)
    objects = schema.get("objects", {})
    for obj_name, obj_spec in objects.items():
        if isinstance(obj_spec, dict):
            # Object-level observable
            if "observable" in obj_spec:
                obs_id = obj_spec["observable"]
                if isinstance(obs_id, int):
                    caption = obj_spec.get("caption", snake_to_pascal(obj_name))
                    observable_types[obs_id] = caption

            # 5. Object attribute observables
            obj_attrs = obj_spec.get("attributes", {})
            for attr_name, attr_def in obj_attrs.items():
                if isinstance(attr_def, dict) and "observable" in attr_def:
                    obs_id = attr_def["observable"]
                    if isinstance(obs_id, int):
                        # Try to get explicit caption first
                        if "caption" in attr_def:
                            caption = attr_def["caption"]
                        else:
                            # Build human-readable caption from object caption
                            obj_caption = obj_spec.get("caption", snake_to_pascal(obj_name))
                            # Special case: if attribute is "uid"
                            if attr_name == "uid":
                                # Check if this caption would conflict with an existing entry
                                # (e.g., user object vs user.uid both become "User")
                                if obj_caption in observable_types.values():
                                    # Add "UID" suffix to avoid conflict
                                    caption = f"{obj_caption} UID"
                                else:
                                    # No conflict, use just the object caption
                                    caption = obj_caption
                            else:
                                # Otherwise: "Object Attribute" (e.g., "Group Name")
                                attr_caption = snake_to_pascal(attr_name)
                                caption = f"{obj_caption} {attr_caption}"
                        observable_types[obs_id] = caption

    # 4 & 6. Scan events for attribute and path-based observables
    events = schema.get("events", {})
    for event_name, event_spec in events.items():
        if isinstance(event_spec, dict):
            # Event attribute observables
            event_attrs = event_spec.get("attributes", {})
            for attr_name, attr_def in event_attrs.items():
                if isinstance(attr_def, dict) and "observable" in attr_def:
                    obs_id = attr_def["observable"]
                    if isinstance(obs_id, int):
                        caption = attr_def.get("caption", f"{event_name}.{attr_name}")
                        observable_types[obs_id] = caption

            # Class-specific attribute path observables
            observables_def = event_spec.get("observables", {})
            if isinstance(observables_def, dict):
                for _path, obs_id in observables_def.items():
                    if isinstance(obs_id, int) and obs_id not in observable_types:
                        # For path-based, we don't have a good caption source
                        # Use a generic label or try to derive from the path
                        # For now, use a placeholder - these are less common
                        observable_types[obs_id] = f"Observable {obs_id}"

    return observable_types
