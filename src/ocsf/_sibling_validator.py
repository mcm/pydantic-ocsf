"""Sibling attribute reconciliation for OCSF models."""

from __future__ import annotations

from typing import Any

from pydantic import model_validator

from ocsf._sibling_enum import SiblingEnum


def create_sibling_reconciler(
    id_field: str, label_field: str, enum_class: type[SiblingEnum]
) -> Any:
    """Create a validator that reconciles sibling ID and label fields.

    OCSF pairs numeric ID fields (foo_id) with string label fields (foo).
    This validator ensures they stay consistent during model initialization.

    Reconciliation scenarios:
    1. Both present + consistent: ✓ Accept
    2. Both present + inconsistent (ID != 99): ✗ Raise ValidationError
    3. Both present + ID=99: ✓ Accept any custom label (Other allows custom values)
    4. Only ID: Extrapolate label from enum (including "Other" for ID=99)
    5. Only label (known): Extrapolate ID from enum
    6. Only label (unknown): Set ID=99 (OTHER)
    7. Neither present: ✓ Accept (both None)

    Args:
        id_field: Name of the ID field (e.g., "activity_id")
        label_field: Name of the label field (e.g., "activity_name")
        enum_class: The enum class for this sibling pair

    Returns:
        Pydantic model_validator decorator

    Example:
        class FileActivity(OCSFBaseModel):
            activity_id: ActivityId | None = None
            activity_name: str | None = None

            _reconcile_activity = create_sibling_reconciler(
                "activity_id", "activity_name", ActivityId
            )
    """

    @model_validator(mode="before")  # type: ignore[misc]
    @classmethod
    def reconcile(cls: type[Any], data: Any) -> Any:
        """Reconcile sibling ID and label fields."""
        if not isinstance(data, dict):
            return data

        id_value = data.get(id_field)
        label_value = data.get(label_field)

        # Also check for Python field name (e.g., "type_" if label_field is "type")
        # This handles the case where user provides type_="value" before normalization
        python_field_name = label_field + "_"
        if label_value is None and python_field_name in data:
            label_value = data.get(python_field_name)
            # Normalize: move the value from python_field_name to label_field
            data[label_field] = label_value
            del data[python_field_name]

        # Case 1 & 6: Both present or both absent - validate consistency
        if id_value is not None and label_value is not None:
            # Special case: ID=99 (Other) allows any custom label
            if id_value == 99:
                return data

            # Validate consistency for all other IDs
            try:
                enum_member = enum_class(id_value)
            except (ValueError, AttributeError):
                # Invalid enum value - let Pydantic handle it during field validation
                return data

            expected_label = enum_member.label
            # Validate consistency (case-insensitive)
            if label_value != expected_label and label_value.lower() != expected_label.lower():
                raise ValueError(
                    f"Inconsistent {id_field}={id_value} and "
                    f"{label_field}={label_value!r} "
                    f"(expected {expected_label!r})"
                )
            return data

        # Case 3: Only ID present - extrapolate label
        if id_value is not None and label_value is None:
            try:
                enum_member = enum_class(id_value)
                data[label_field] = enum_member.label
            except (ValueError, AttributeError):
                # Invalid enum value - set label to string of ID
                data[label_field] = str(id_value)
            return data

        # Case 4 & 5: Only label present - extrapolate ID
        if label_value is not None and id_value is None:
            try:
                # Try to find matching enum member
                enum_member = enum_class.from_label(label_value)
                data[id_field] = enum_member.value
            except ValueError:
                # Unknown label - map to OTHER (99)
                data[id_field] = 99
                # Keep the original label
            return data

        # Case 6: Neither present
        return data

    return reconcile
