"""Dynamic enum creation for OCSF sibling attributes."""

from __future__ import annotations

from typing import Any

from ocsf._sibling_enum import SiblingEnum


def create_sibling_enum(
    name: str, values: dict[int, str], parent_class_name: str
) -> type[SiblingEnum]:
    """Create a SiblingEnum subclass dynamically.

    Args:
        name: Name of the enum class (e.g., "ActivityId")
        values: Mapping of enum values to labels (e.g., {1: "Create", 4: "Delete"})
        parent_class_name: Name of the parent model (e.g., "FileActivity")

    Returns:
        Dynamically created SiblingEnum subclass

    Example:
        ActivityId = create_sibling_enum(
            "ActivityId",
            {1: "Create", 4: "Delete", 99: "Other"},
            "FileActivity"
        )

        # Usage:
        ActivityId.CREATE      # == 1
        ActivityId(1)          # CREATE
        ActivityId("Create")   # CREATE
        ActivityId.CREATE.label  # "Create"
    """
    from ocsf._utils import label_to_enum_name

    # Create enum members
    members = {}
    for value, label in values.items():
        # Convert label to valid enum member name (e.g., "Create" -> "CREATE")
        member_name = label_to_enum_name(label)
        members[member_name] = value

    # Always include OTHER = 99 if not present
    if 99 not in values and "OTHER" not in members:
        members["OTHER"] = 99
        values[99] = "Other"

    # Create the enum class using functional API
    # mypy doesn't understand enum functional API, but it works at runtime
    enum_cls = SiblingEnum(name, members)  # type: ignore

    # Inject the label map as a class method
    enum_cls._get_label_map = classmethod(lambda cls: values)  # type: ignore

    # Set module for better repr
    enum_cls.__module__ = f"ocsf.{parent_class_name.lower()}"

    return enum_cls  # type: ignore


def extract_inline_enums(
    attributes: dict[str, Any], dictionary: dict[str, Any]
) -> dict[str, tuple[dict[int, str], str | None]]:
    """Extract inline enum definitions from attributes.

    Args:
        attributes: Object/event attributes from schema
        dictionary: Schema dictionary for shared definitions

    Returns:
        Dictionary mapping field names to (enum_values, field_name_id) tuples
        where enum_values is {int: label} and field_name_id is the sibling ID field

    Example:
        {
            "activity_id": ({1: "Create", 4: "Delete"}, "activity_id"),
            "severity_id": ({1: "Info", 2: "Low"}, "severity_id"),
        }
    """
    inline_enums = {}
    dict_attributes = dictionary.get("attributes", {})

    for field_name, field_spec in attributes.items():
        # Skip non-dict specs
        if not isinstance(field_spec, dict):
            continue

        # Merge with dictionary definition
        if field_name in dict_attributes:
            merged_spec = {**dict_attributes[field_name], **field_spec}
        else:
            merged_spec = field_spec

        # Check if this field has an enum
        enum_def = merged_spec.get("enum")
        if not enum_def:
            continue

        # Extract enum values
        enum_values = {}
        for value_key, value_data in enum_def.items():
            try:
                # value_key is like "1", "4", "99"
                int_value = int(value_key)
                # value_data has 'caption' for the label
                label = value_data.get("caption", str(int_value))
                enum_values[int_value] = label
            except (ValueError, AttributeError):
                # Skip invalid enum values
                continue

        if enum_values:
            # Determine if this is a sibling ID field
            # ID fields end with _id
            sibling_id = field_name if field_name.endswith("_id") else None
            inline_enums[field_name] = (enum_values, sibling_id)

    return inline_enums
