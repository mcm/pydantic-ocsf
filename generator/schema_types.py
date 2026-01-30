"""Data structures representing OCSF schema components."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Requirement(Enum):
    """OCSF field requirement levels."""

    REQUIRED = "required"
    RECOMMENDED = "recommended"
    OPTIONAL = "optional"


@dataclass
class SchemaAttribute:
    """An attribute (field) in an OCSF object or event."""

    name: str
    type: str
    description: str = ""
    requirement: Requirement = Requirement.OPTIONAL
    is_array: bool = False
    object_type: str | None = None  # For object references
    enum: dict[str, Any] | None = None  # Inline enum definition
    sibling: str | None = None  # Related enum field (e.g., activity_id for activity_name)

    @classmethod
    def from_dict(
        cls,
        name: str,
        data: dict[str, Any],
        dictionary_attr: dict[str, Any] | None = None,
        available_objects: set[str] | None = None,
    ) -> SchemaAttribute:
        """Create from OCSF schema dictionary.

        Args:
            name: Attribute name
            data: Local attribute definition (may be partial)
            dictionary_attr: Global attribute definition from dictionary (if exists)
            available_objects: Set of valid object names for type detection
        """
        # Merge dictionary definition with local override
        merged = {}
        if dictionary_attr and isinstance(dictionary_attr, dict):
            merged.update(dictionary_attr)
        if isinstance(data, dict):
            merged.update(data)
        else:
            # If data is not a dict (e.g., just a string or other type), use dictionary only
            pass

        requirement = Requirement.OPTIONAL
        if merged.get("requirement") == "required":
            requirement = Requirement.REQUIRED
        elif merged.get("requirement") == "recommended":
            requirement = Requirement.RECOMMENDED

        # Extract type information
        type_value = merged.get("type", "string_t")
        object_type_value = merged.get("object_type")

        # Detect if type is an object name (CORE FIX)
        if available_objects and type_value in available_objects and not object_type_value:
            object_type_value = type_value
            type_value = "object_t"  # Normalize to object_t

        return cls(
            name=name,
            type=type_value,
            description=merged.get("description", ""),
            requirement=requirement,
            is_array=merged.get("is_array", False),
            object_type=object_type_value,
            enum=merged.get("enum"),
            sibling=merged.get("sibling"),
        )


@dataclass
class SchemaEnum:
    """An OCSF enumeration."""

    name: str
    description: str = ""
    values: dict[int, str] = field(default_factory=dict)  # value -> name
    value_descriptions: dict[int, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, name: str, data: dict[str, Any]) -> SchemaEnum:
        """Create from OCSF schema dictionary."""
        values = {}
        value_descriptions = {}

        enum_data = data.get("enum", {})
        for str_val, val_info in enum_data.items():
            try:
                int_val = int(str_val)
            except ValueError:
                continue

            if isinstance(val_info, dict):
                # OCSF uses "caption" for the label, not "name"
                values[int_val] = val_info.get("caption", val_info.get("name", f"VALUE_{int_val}"))
                value_descriptions[int_val] = val_info.get("description", "")
            else:
                values[int_val] = str(val_info)

        return cls(
            name=name,
            description=data.get("description", ""),
            values=values,
            value_descriptions=value_descriptions,
        )


@dataclass
class SchemaObject:
    """An OCSF object definition."""

    name: str
    caption: str = ""
    description: str = ""
    extends: str | None = None
    attributes: dict[str, SchemaAttribute] = field(default_factory=dict)

    @classmethod
    def from_dict(
        cls,
        name: str,
        data: dict[str, Any],
        dictionary: dict[str, Any] | None = None,
        available_objects: set[str] | None = None,
    ) -> SchemaObject:
        """Create from OCSF schema dictionary."""
        attributes = {}
        dict_attrs = dictionary.get("attributes", {}) if dictionary else {}

        for attr_name, attr_data in data.get("attributes", {}).items():
            # Get dictionary definition if it exists
            dictionary_attr = dict_attrs.get(attr_name)
            attributes[attr_name] = SchemaAttribute.from_dict(
                attr_name, attr_data, dictionary_attr, available_objects
            )

        return cls(
            name=name,
            caption=data.get("caption", ""),
            description=data.get("description", ""),
            extends=data.get("extends"),
            attributes=attributes,
        )


@dataclass
class SchemaEvent:
    """An OCSF event class definition."""

    name: str
    caption: str = ""
    description: str = ""
    uid: int = 0
    category: str = ""
    category_uid: int = 0
    extends: str | None = None
    attributes: dict[str, SchemaAttribute] = field(default_factory=dict)

    @classmethod
    def from_dict(
        cls,
        name: str,
        data: dict[str, Any],
        dictionary: dict[str, Any] | None = None,
        available_objects: set[str] | None = None,
    ) -> SchemaEvent:
        """Create from OCSF schema dictionary."""
        attributes = {}
        dict_attrs = dictionary.get("attributes", {}) if dictionary else {}

        for attr_name, attr_data in data.get("attributes", {}).items():
            # Get dictionary definition if it exists
            dictionary_attr = dict_attrs.get(attr_name)
            attributes[attr_name] = SchemaAttribute.from_dict(
                attr_name, attr_data, dictionary_attr, available_objects
            )

        return cls(
            name=name,
            caption=data.get("caption", ""),
            description=data.get("description", ""),
            uid=data.get("uid", 0),
            category=data.get("category", ""),
            category_uid=data.get("category_uid", 0),
            extends=data.get("extends"),
            attributes=attributes,
        )


@dataclass
class ParsedSchema:
    """Complete parsed OCSF schema."""

    version: str
    events: dict[str, SchemaEvent] = field(default_factory=dict)
    objects: dict[str, SchemaObject] = field(default_factory=dict)
    enums: dict[str, SchemaEnum] = field(default_factory=dict)
