"""Parse OCSF schema into typed data structures."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from generator.schema_fetcher import fetch_schema
from generator.schema_types import (
    ParsedSchema,
    SchemaAttribute,
    SchemaEnum,
    SchemaEvent,
    SchemaObject,
)


def parse_schema(version: str, cache_dir: Path | None = None) -> ParsedSchema:
    """Fetch and parse OCSF schema into typed structures.

    Args:
        version: OCSF version (e.g., "v1.2.0")
        cache_dir: Optional cache directory for downloaded schema

    Returns:
        ParsedSchema with all events, objects, and enums
    """
    raw_schema = fetch_schema(version, cache_dir)

    parsed = ParsedSchema(version=version)

    # Get the dictionary for attribute definitions
    dictionary = raw_schema.get("dictionary")

    # Build object name registry for type detection
    available_objects = set(raw_schema.get("objects", {}).keys())

    # Parse objects first (events may reference them)
    for name, obj_data in raw_schema.get("objects", {}).items():
        parsed.objects[name] = SchemaObject.from_dict(name, obj_data, dictionary, available_objects)

    # Parse events
    for name, event_data in raw_schema.get("events", {}).items():
        parsed.events[name] = SchemaEvent.from_dict(name, event_data, dictionary, available_objects)

    # Parse global enums from dictionary
    for name, enum_data in raw_schema.get("enums", {}).items():
        if name not in parsed.enums:
            parsed.enums[name] = SchemaEnum.from_dict(name, enum_data)

    # Resolve inheritance FIRST
    _resolve_object_inheritance(parsed)
    _resolve_event_inheritance(parsed)

    # Extract inline enums AFTER inheritance (so we see all inherited attributes)
    for name, obj in parsed.objects.items():
        _extract_inline_enums_from_parsed(parsed, name, obj.attributes)

    for name, event in parsed.events.items():
        _extract_inline_enums_from_parsed(parsed, name, event.attributes)

    return parsed


def _extract_inline_enums_from_parsed(
    parsed: ParsedSchema,
    parent_name: str,
    attributes: dict[str, SchemaAttribute],
) -> None:
    """Extract inline enum definitions from parsed attributes.

    Inline enums are namespaced by their parent class to avoid collisions.
    For example, incident_finding.status_id becomes 'incident_finding_status_id'.

    This runs AFTER inheritance resolution so we see all inherited attributes.
    """
    for attr_name, attr in attributes.items():
        # Check if attribute has an inline enum definition
        if attr.enum and isinstance(attr.enum, dict):
            # Create namespaced enum name: parent_class_attribute_name
            enum_name = f"{parent_name}_{attr_name}"

            if enum_name not in parsed.enums:
                # Create a temporary dict with enum structure for SchemaEnum.from_dict
                enum_dict = {
                    "enum": attr.enum,
                    "description": attr.description,
                }
                parsed.enums[enum_name] = SchemaEnum.from_dict(enum_name, enum_dict)


def _resolve_object_inheritance(parsed: ParsedSchema) -> None:
    """Resolve object inheritance, merging parent attributes into children."""

    def resolve_object(obj: SchemaObject, visited: set[str]) -> dict[str, SchemaAttribute]:
        if obj.name in visited:
            return obj.attributes
        visited.add(obj.name)

        if obj.extends and obj.extends in parsed.objects:
            parent = parsed.objects[obj.extends]
            parent_attrs = resolve_object(parent, visited)
            # Parent attributes + child attributes (child overrides parent)
            merged = dict(parent_attrs)
            merged.update(obj.attributes)
            obj.attributes = merged

        return obj.attributes

    for obj in parsed.objects.values():
        resolve_object(obj, set())


def _resolve_event_inheritance(parsed: ParsedSchema) -> None:
    """Resolve event inheritance, merging parent attributes into children."""

    def resolve_event(event: SchemaEvent, visited: set[str]) -> dict[str, SchemaAttribute]:
        if event.name in visited:
            return event.attributes
        visited.add(event.name)

        if event.extends and event.extends in parsed.events:
            parent = parsed.events[event.extends]
            parent_attrs = resolve_event(parent, visited)
            merged = dict(parent_attrs)
            merged.update(event.attributes)
            event.attributes = merged

        return event.attributes

    for event in parsed.events.values():
        resolve_event(event, set())


def print_schema_summary(schema: ParsedSchema) -> None:
    """Print a summary of the parsed schema."""
    print(f"\nParsed Schema {schema.version}")
    print(f"  Events: {len(schema.events)}")
    print(f"  Objects: {len(schema.objects)}")
    print(f"  Enums: {len(schema.enums)}")

    if schema.events:
        print("\n  Sample events:")
        for name in list(schema.events.keys())[:5]:
            event = schema.events[name]
            print(f"    - {name} (uid={event.uid}, attrs={len(event.attributes)})")

    if schema.objects:
        print("\n  Sample objects:")
        for name in list(schema.objects.keys())[:5]:
            obj = schema.objects[name]
            print(f"    - {name} (attrs={len(obj.attributes)})")

    if schema.enums:
        print("\n  Sample enums:")
        for name in list(schema.enums.keys())[:5]:
            enum = schema.enums[name]
            print(f"    - {name} ({len(enum.values)} values)")


if __name__ == "__main__":
    import sys

    version = sys.argv[1] if len(sys.argv) > 1 else "v1.2.0"
    cache = Path(".schema_cache")

    schema = parse_schema(version, cache_dir=cache)
    print_schema_summary(schema)
