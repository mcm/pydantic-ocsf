"""Field name normalization for OCSF models."""

from __future__ import annotations

from typing import Any

from pydantic import model_validator


def create_normalizer() -> Any:
    """Create a validator that normalizes Python field names to OCSF aliases.

    This ensures that when both field name (type_) and alias (type) are valid inputs
    (via populate_by_name=True), we consistently use the alias name. This prevents
    duplicate keys in the data dict and ensures proper interaction with sibling
    reconciliation validators.

    Returns:
        Pydantic model_validator that normalizes field names

    Example:
        Input:  {"type_": "Risk", "type_id": 99}
        Output: {"type": "Risk", "type_id": 99}
    """

    @model_validator(mode="before")  # type: ignore[misc]
    @classmethod
    def normalize(cls: type[Any], data: Any) -> Any:
        """Normalize Python field names with aliases to use the alias consistently."""
        if not isinstance(data, dict):
            return data

        # Build mapping: Python field name -> alias (for fields that have aliases)
        field_to_alias = {}
        for field_name, field_info in cls.model_fields.items():
            # Only map if they have an alias and are different (e.g., "type_" -> "type", not "name" -> "name")
            if (
                field_info.validation_alias
                and isinstance(field_info.validation_alias, str)
                and field_name != field_info.validation_alias
            ):
                field_to_alias[field_name] = field_info.validation_alias

        # If there are no fields with aliases, return data as-is
        if not field_to_alias:
            return data

        # Convert Python field names to their aliases
        normalized = {}
        for key, value in data.items():
            if key in field_to_alias:
                # Use alias instead of Python field name
                alias_key = field_to_alias[key]
                normalized[alias_key] = value
            else:
                normalized[key] = value

        return normalized

    return normalize
