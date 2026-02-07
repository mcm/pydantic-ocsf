#!/usr/bin/env python3
"""Regenerate type stub files (.pyi) for all OCSF versions.

This is a standalone script that doesn't depend on pydantic being installed.
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Optional

# Ensure UTF-8 encoding for stdout on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def snake_to_pascal(name: str) -> str:
    """Convert snake_case to PascalCase."""
    return "".join(word.capitalize() for word in name.split("_"))


def label_to_enum_name(label: str) -> str:
    """Convert enum label to UPPER_SNAKE_CASE member name."""
    name = re.sub(r"[\s\-]+", "_", label)
    name = re.sub(r"[^a-zA-Z0-9_]", "", name)
    name = name.upper().strip("_")
    name = re.sub(r"_+", "_", name)

    if name and name[0].isdigit():
        name = f"VALUE_{name}"

    return name or "UNKNOWN"


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
    """
    if not id_field.endswith("_id"):
        raise ValueError(f"Expected field ending in '_id', got {id_field!r}")

    # Remove "_id" suffix to get base name
    base = id_field[:-3]

    # Python reserved keywords that need underscore suffix
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

    # Check if base name is a reserved keyword
    if base in RESERVED_KEYWORDS or base.lower() in {k.lower() for k in RESERVED_KEYWORDS}:
        return f"{base}_"

    return base


def pascal_to_snake(name: str) -> str:
    """Convert PascalCase to snake_case.

    Examples:
        ActivityId -> activity_id
        SeverityId -> severity_id
        TypeId -> type_id
    """
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def generate_objects_stub(version: str, schema: dict[str, Any], output_dir: Path) -> None:
    """Generate objects.pyi stub file."""
    lines = [
        '"""OCSF Objects - Type stubs (auto-generated)."""',
        "",
        "from __future__ import annotations",
        "",
        "from typing import Any",
        "",
        "from typing_extensions import Self",
        "",
        "from ocsf._base import OCSFBaseModel",
        "from ocsf._sibling_enum import SiblingEnum",
        "",
    ]

    dict_attributes = schema.get("dictionary", {}).get("attributes", {})
    all_objects = schema.get("objects", {})

    # Generate ONLY object stubs
    for obj_name, obj_spec in sorted(all_objects.items()):
        lines.extend(
            _generate_class_stub(obj_name, obj_spec, dict_attributes, all_objects, is_event=False)
        )
        lines.append("")

    output_path = output_dir / "objects.pyi"
    output_path.write_text("\n".join(lines))
    print(f"  Generated objects.pyi: {len(lines)} lines")


def generate_events_stub(version: str, schema: dict[str, Any], output_dir: Path) -> None:
    """Generate events.pyi stub file."""
    lines = [
        '"""OCSF Events - Type stubs (auto-generated)."""',
        "",
        "from __future__ import annotations",
        "",
        "from typing import Any",
        "",
        "from typing_extensions import Self",
        "",
        "from ocsf._base import OCSFBaseModel",
        "from ocsf._sibling_enum import SiblingEnum",
        "",
    ]

    dict_attributes = schema.get("dictionary", {}).get("attributes", {})
    all_events = schema.get("events", {})

    # Generate ONLY event stubs
    for event_name, event_spec in sorted(all_events.items()):
        lines.extend(
            _generate_class_stub(event_name, event_spec, dict_attributes, all_events, is_event=True)
        )
        lines.append("")

    output_path = output_dir / "events.pyi"
    output_path.write_text("\n".join(lines))
    print(f"  Generated events.pyi: {len(lines)} lines")


def generate_init_stub(version: str, schema: dict[str, Any], output_dir: Path) -> None:
    """Generate __init__.pyi that only exposes namespace modules."""
    lines = [
        '"""OCSF Models - Type stubs (auto-generated)."""',
        "",
        "from __future__ import annotations",
        "",
        "# Namespace modules only - import from .objects or .events",
        "from . import events as events",
        "from . import objects as objects",
        "",
        "__all__ = ['objects', 'events']",
    ]

    output_path = output_dir / "__init__.pyi"
    output_path.write_text("\n".join(lines))
    print(f"  Generated __init__.pyi: {len(lines)} lines")


def _get_parent_requirement(
    field_name: str,
    spec: dict[str, Any],
    dict_attributes: dict[str, Any],
    all_specs: dict[str, Any],
) -> Optional[str]:
    """Get the requirement status of a field from parent class hierarchy.

    Returns 'required', 'optional', 'recommended', or None if field not found in parent.
    """
    if "extends" not in spec:
        return None

    parent_name = spec["extends"]

    # Recursively check parent hierarchy
    while parent_name:
        parent_spec = all_specs.get(parent_name, {})
        parent_attrs = parent_spec.get("attributes", {})

        if field_name in parent_attrs:
            parent_field = parent_attrs[field_name]
            if isinstance(parent_field, dict):
                # Merge with dictionary to get full spec
                merged = {**dict_attributes.get(field_name, {}), **parent_field}
                if "requirement" in merged:
                    req: Optional[str] = merged.get("requirement")
                    return req

        # Move up the hierarchy
        parent_name = parent_spec.get("extends")

    return None


def _generate_class_stub(
    name: str,
    spec: dict[str, Any],
    dict_attributes: dict[str, Any],
    all_specs: dict[str, Any],
    is_event: bool = False,
) -> list[str]:
    """Generate stub lines for a single class."""
    lines = []

    # Class declaration
    model_name = snake_to_pascal(name)

    if "extends" in spec:
        base_name = snake_to_pascal(spec["extends"])
        lines.append(f"class {model_name}({base_name}):")
    else:
        lines.append(f"class {model_name}(OCSFBaseModel):")

    # Extract and generate enums
    attributes = spec.get("attributes", {})
    enums_to_generate = []

    for field_name, field_spec in attributes.items():
        if not isinstance(field_spec, dict):
            continue

        # Merge with dictionary
        merged_spec = {**dict_attributes.get(field_name, {}), **field_spec}

        # Check for sibling enum
        if "enum" in merged_spec and field_name.endswith("_id"):
            enum_name = snake_to_pascal(field_name)
            enum_values = merged_spec["enum"]
            enums_to_generate.append((enum_name, enum_values))

    # Generate nested enum classes and track sibling ID fields
    sibling_id_fields = []  # Track ID fields that have enums
    for enum_name, enum_values in enums_to_generate:
        lines.append(f"    class {enum_name}(SiblingEnum):")

        # Generate enum members with actual values
        for value_key, value_data in sorted(enum_values.items(), key=lambda x: int(x[0])):
            try:
                int_value = int(value_key)
                label = value_data.get("caption", str(int_value))
                member_name = label_to_enum_name(label)
                lines.append(f"        {member_name} = {int_value}")
            except (ValueError, AttributeError):
                continue

        # Add OTHER if not present
        if "99" not in enum_values:
            lines.append("        OTHER = 99")

        lines.append("        @property")
        lines.append("        def label(self) -> str: ...")
        lines.append("        @classmethod")
        lines.append("        def from_label(cls, label: str) -> Self: ...")
        lines.append("")

        # Track the field name this enum is for (e.g., ActivityId -> activity_id)
        field_name = pascal_to_snake(enum_name)
        if field_name.endswith("_id"):
            sibling_id_fields.append(field_name)

    # Generate field stubs
    has_fields = False
    processed_fields = set()  # Track which fields we've already generated
    RESERVED = {"class", "type", "import", "from", "def", "return", "if", "else"}

    for field_name, field_spec in sorted(attributes.items()):
        if not isinstance(field_spec, dict) or field_name.startswith("$"):
            continue

        if field_name in RESERVED:
            continue  # Skip reserved keywords

        # Merge with dictionary
        merged_spec = {**dict_attributes.get(field_name, {}), **field_spec}

        # Check if field only provides enum metadata (child extending parent's field)
        has_enum = "enum" in merged_spec and field_name.endswith("_id")
        only_enum = has_enum and "requirement" not in field_spec and "extends" in spec

        # Skip field if it only provides enum (inherits from parent)
        # But keep the enum class which was already generated above
        if only_enum:
            # Check if parent actually defines this field
            parent_req = _get_parent_requirement(field_name, spec, dict_attributes, all_specs)
            if parent_req is not None:
                # Parent defines it, skip redefinition
                continue

        # Build type annotation - use int for enum fields to avoid mypy variance issues
        # The enum classes are available for IDE autocomplete, runtime uses int/IntEnum
        # Use int type annotation (SiblingEnum extends IntEnum extends int)
        # This avoids mypy errors about incompatible enum types in inheritance
        type_annotation = "int" if has_enum else _build_type_annotation(field_name, merged_spec)

        is_required = merged_spec.get("requirement") == "required"

        # Make UID fields optional for events (they're auto-filled by validators)
        if is_event and field_name in ("category_uid", "class_uid", "type_uid"):
            is_required = False

        # Add None for optional fields if not already included
        if not is_required and "| None" not in type_annotation:
            type_annotation = f"{type_annotation} | None"

        if is_required:
            lines.append(f"    {field_name}: {type_annotation}")
        else:
            lines.append(f"    {field_name}: {type_annotation} = None")

        has_fields = True
        processed_fields.add(field_name)

    # After all schema fields, add inferred sibling label fields
    for id_field in sibling_id_fields:
        label_field = infer_sibling_label_field(id_field)

        # Only add if not already processed (some are explicit in schema)
        if label_field not in processed_fields:
            # Add as optional string field
            lines.append(f"    {label_field}: str | None = None")
            has_fields = True
            processed_fields.add(label_field)

    # If no fields or enums, add pass
    if not has_fields and not enums_to_generate:
        lines.append("    pass")

    return lines


def _build_type_annotation(field_name: str, spec: dict[str, Any]) -> str:
    """Build type annotation for a field."""
    ocsf_type = spec.get("type", "string_t")
    is_array = spec.get("is_array", False)
    is_required = spec.get("requirement") == "required"

    # Map OCSF types to Python types
    type_map = {
        "string_t": "str",
        "integer_t": "int",
        "long_t": "int",
        "float_t": "float",
        "boolean_t": "bool",
        "timestamp_t": "int",
        "datetime_t": "str",
        "json_t": "dict[str, Any]",
        "object_t": "dict[str, Any]",
    }

    # Check if it's an object reference
    if "object_type" in spec:
        python_type = snake_to_pascal(spec["object_type"])
    elif ocsf_type in type_map:
        python_type = type_map[ocsf_type]
    else:
        python_type = "Any"

    # Handle arrays
    if is_array:
        python_type = f"list[{python_type}]"

    # Add None for optional fields
    if not is_required:
        python_type = f"{python_type} | None"

    return python_type


def main() -> None:
    """Main entry point."""
    # Find schema files
    schema_dir = Path(__file__).parent.parent / "src" / "ocsf" / "schemas"

    if not schema_dir.exists():
        print(f"Error: Schema directory not found: {schema_dir}")
        print("Run scripts/download_schemas.py first")
        return

    print("Regenerating type stubs...")
    print("=" * 70)

    # Process each version
    for schema_file in sorted(schema_dir.glob("v*.json")):
        version_str = schema_file.stem  # e.g., "v1_7_0"
        version = version_str.lstrip("v").replace("_", ".")  # e.g., "1.7.0"

        # Load schema
        with open(schema_file) as f:
            schema = json.load(f)

        # Generate stub files
        stub_dir = schema_dir.parent / version_str.replace("-", "_")
        stub_dir.mkdir(exist_ok=True)

        print(f"\n{version_str} (OCSF v{version}):")

        # Generate 3 files: objects.pyi, events.pyi, __init__.pyi
        generate_objects_stub(version, schema, stub_dir)
        generate_events_stub(version, schema, stub_dir)
        generate_init_stub(version, schema, stub_dir)

    print("\n" + "=" * 70)
    print("✅ Stub generation complete!")


if __name__ == "__main__":
    main()
