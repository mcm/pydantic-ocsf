"""Base class for OCSF sibling enums with string label support.

OCSF frequently pairs numeric ID fields (foo_id) with string label fields (foo).
This module provides a base enum class that enables construction from either form
and provides the canonical label for any enum value.
"""

from __future__ import annotations

import sys
from enum import IntEnum

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class SiblingEnum(IntEnum):
    """Base class for OCSF sibling enums with string label support.

    OCSF pairs numeric ID fields (foo_id) with string label fields (foo).
    This base class enables construction from either form and provides
    the canonical label for any enum value.

    Subclasses should override `_get_label_map()` to provide the mapping
    of integer values to canonical string labels.

    Example:
        class ActivityId(SiblingEnum):
            CREATE = 1
            DELETE = 4
            OTHER = 99

            @classmethod
            def _get_label_map(cls) -> dict[int, str]:
                return {
                    1: "Create",
                    4: "Delete",
                    99: "Other",
                }

        # All equivalent:
        ActivityId.CREATE
        ActivityId(1)
        ActivityId("Create")
        ActivityId("create")  # case-insensitive

        # Unknown strings raise ValueError (strict for programmer errors):
        ActivityId("Custom Action")  # Raises ValueError!
    """

    @classmethod
    def _get_label_map(cls) -> dict[int, str]:
        """Get the mapping of enum values to labels.

        This method should be overridden by subclasses to provide the
        label mapping. The base implementation returns an empty dict.

        Returns:
            Dictionary mapping integer enum values to canonical string labels
        """
        return {}

    @property
    def label(self) -> str:
        """Return the canonical human-readable label for this value.

        Returns:
            The canonical label string for this enum value.
            If the value is not in the label map, returns the stringified value.

        Example:
            >>> ActivityId.CREATE.label
            'Create'
            >>> ActivityId(1).label
            'Create'
        """
        label_map = self.__class__._get_label_map()
        return label_map.get(self.value, str(self.value))

    @classmethod
    def from_label(cls, label: str) -> Self:
        """Create enum from string label (case-insensitive).

        Args:
            label: Human-readable label (e.g., "Create", "create", "CREATE")

        Returns:
            The matching enum member

        Raises:
            ValueError: If label doesn't match any known enum value

        Example:
            >>> ActivityId.from_label("Create")
            <ActivityId.CREATE: 1>
            >>> ActivityId.from_label("create")
            <ActivityId.CREATE: 1>
        """
        normalized = label.lower()
        label_map = cls._get_label_map()
        for value, lbl in label_map.items():
            if lbl.lower() == normalized:
                return cls(value)
        raise ValueError(f"Unknown {cls.__name__} label: {label!r}")

    @classmethod
    def _missing_(cls, value: object) -> Self:
        """Handle construction from string labels.

        This method is called by the enum machinery when a value is not found
        among the existing enum members. We use it to support string label lookup.

        Direct enum construction is STRICT - unknown values always raise ValueError.
        This catches programmer errors. Only during JSON parsing (via sibling
        reconciliation) should unknown values map to OTHER.

        Args:
            value: The value that was not found (typically a string label)

        Returns:
            The enum member corresponding to the label

        Raises:
            ValueError: If the value is a string that doesn't match any label,
                       or if the value is not a valid integer or string
        """
        if isinstance(value, str):
            # Try case-insensitive label lookup
            return cls.from_label(value)  # Raises ValueError if not found
        # Not a string and not a valid member - let the standard error occur
        raise ValueError(f"{value!r} is not a valid {cls.__name__}")

    def __new__(cls, value: int | str) -> Self:
        """Create enum member from integer or string value.

        This is called during class definition to create enum members, and also
        when constructing enum instances. Accepts both integers and string labels
        thanks to the _missing_ method which handles string lookup.

        Note: The type signature declares int | str for external callers, but
        _missing_ ensures only int values reach this method's implementation.

        Args:
            value: Integer enum value or string label

        Returns:
            The enum member
        """
        # _missing_ handles string conversion, so by the time we get here,
        # value should always be an int
        obj = int.__new__(cls, value)
        assert isinstance(value, int)
        obj._value_ = value  # pyright: ignore[reportAttributeAccessIssue]
        return obj
