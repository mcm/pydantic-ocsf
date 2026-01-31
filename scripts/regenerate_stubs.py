#!/usr/bin/env python3
"""Regenerate type stub files (.pyi) for all OCSF versions.

This is a standalone script that doesn't depend on pydantic being installed.
"""

import json
import re
from pathlib import Path
from typing import Any


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


def generate_stub_for_version(version: str, schema: dict[str, Any], output_path: Path) -> None:
    """Generate stub file for a single version."""
    lines = [
        '"""Type stubs for OCSF models (auto-generated)."""',
        "",
        "from __future__ import annotations",
        "",
        "from typing import Any",
        "from typing_extensions import Self",
        "from enum import IntEnum",
        "from pydantic import BaseModel, Field",
        "from ocsf._base import OCSFBaseModel",
        "from ocsf._sibling_enum import SiblingEnum",
        "",
    ]

    dict_attributes = schema.get("dictionary", {}).get("attributes", {})

    # Generate object stubs
    for obj_name, obj_spec in sorted(schema.get("objects", {}).items()):
        lines.extend(_generate_class_stub(obj_name, obj_spec, dict_attributes))
        lines.append("")

    # Generate event stubs
    for event_name, event_spec in sorted(schema.get("events", {}).items()):
        lines.extend(_generate_class_stub(event_name, event_spec, dict_attributes))
        lines.append("")

    # Write stub file
    output_path.write_text("\n".join(lines))
    print(f"  Generated {output_path.name}: {len(lines)} lines")


def _generate_class_stub(
    name: str, spec: dict[str, Any], dict_attributes: dict[str, Any]
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

    # Generate nested enum classes
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
        lines.append("        def from_label(cls, label: str) -> Self: ...")  # type: ignore
        lines.append("")

    # Generate field stubs
    has_fields = False
    RESERVED = {"class", "type", "import", "from", "def", "return", "if", "else"}

    for field_name, field_spec in sorted(attributes.items()):
        if not isinstance(field_spec, dict) or field_name.startswith("$"):
            continue

        if field_name in RESERVED:
            continue  # Skip reserved keywords

        # Merge with dictionary
        merged_spec = {**dict_attributes.get(field_name, {}), **field_spec}

        # Build type annotation
        type_annotation = _build_type_annotation(field_name, merged_spec)
        is_required = merged_spec.get("requirement") == "required"

        if is_required:
            lines.append(f"    {field_name}: {type_annotation}")
        else:
            lines.append(f"    {field_name}: {type_annotation} = None")

        has_fields = True

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
        version = version_str.replace("v", "").replace("_", ".")  # e.g., "1.7.0"

        # Load schema
        with open(schema_file) as f:
            schema = json.load(f)

        # Generate stub file
        stub_dir = schema_dir.parent / version_str
        stub_dir.mkdir(exist_ok=True)
        stub_file = stub_dir / "__init__.pyi"

        print(f"\n{version_str} (OCSF v{version}):")
        generate_stub_for_version(version, schema, stub_file)

    print("\n" + "=" * 70)
    print("✅ Stub generation complete!")


if __name__ == "__main__":
    main()
