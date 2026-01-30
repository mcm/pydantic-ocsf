"""Peripheral Device object."""

from __future__ import annotations

from typing import Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum


class PeripheralDevice(OCSFBaseModel):
    """The peripheral device object describes the properties of external, connectable, and detachable hardware.

    See: https://schema.ocsf.io/1.7.0/objects/peripheral_device
    """

    # Nested Enums for sibling attribute pairs
    class TypeId(SiblingEnum):
        """The normalized peripheral device type ID.

        OCSF Attribute: type_id
        """

        UNKNOWN = 0
        EXTERNAL_STORAGE = 1
        KEYBOARD = 2
        MOUSE = 3
        PRINTER = 4
        MONITOR = 5
        MICROPHONE = 6
        WEBCAM = 7
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "External Storage",
                2: "Keyboard",
                3: "Mouse",
                4: "Printer",
                5: "Monitor",
                6: "Microphone",
                7: "Webcam",
                99: "Other",
            }

    name: str = Field(..., description="The name of the peripheral device.")
    class_: str | None = Field(default=None, description="The class of the peripheral device.")
    model: str | None = Field(
        default=None, description="The peripheral device model. [Recommended]"
    )
    serial_number: str | None = Field(
        default=None, description="The peripheral device serial number. [Recommended]"
    )
    type_: str | None = Field(
        default=None,
        description="The Peripheral Device type, normalized to the caption of the <code>type_id</code> value. In the case of 'Other', it is defined by the source.",
    )
    type_id: TypeId | None = Field(
        default=None, description="The normalized peripheral device type ID. [Recommended]"
    )
    uid: str | None = Field(
        default=None, description="The unique identifier of the peripheral device. [Recommended]"
    )
    vendor_id_list: list[str] | None = Field(
        default=None, description="The list of vendor IDs for the peripheral device. [Recommended]"
    )
    vendor_name: str | None = Field(
        default=None, description="The primary vendor name for the peripheral device. [Recommended]"
    )

    @model_validator(mode="before")
    @classmethod
    def _reconcile_siblings(cls, data: Any) -> Any:
        """Reconcile sibling attribute pairs during parsing.

        For each sibling pair (e.g., activity_id/activity_name):
        - If both present: validate they match, use canonical label casing
        - If only ID: extrapolate label from enum
        - If only label: extrapolate ID from enum (unknown → OTHER=99)
        - If neither: leave for field validation to handle required/optional
        """
        if not isinstance(data, dict):
            return data

        # Sibling pairs for this object class
        siblings: list[tuple[str, str, type[SiblingEnum]]] = [
            ("type_id", "type", cls.TypeId),
        ]

        for id_field, label_field, enum_cls in siblings:
            id_val = data.get(id_field)
            label_val = data.get(label_field)

            has_id = id_val is not None
            has_label = label_val is not None

            if has_id and has_label:
                # Both present: validate consistency
                assert id_val is not None  # Type narrowing for mypy
                try:
                    enum_member = enum_cls(id_val)
                except (ValueError, KeyError) as e:
                    raise ValueError(f"Invalid {id_field} value: {id_val}") from e

                expected_label = enum_member.label

                # OTHER (99) allows any custom label
                if enum_member.value != 99:
                    if expected_label.lower() != str(label_val).lower():
                        raise ValueError(
                            f"{id_field}={id_val} ({expected_label}) "
                            f"does not match {label_field}={label_val!r}"
                        )
                    # Use canonical label casing
                    data[label_field] = expected_label
                # For OTHER, preserve the custom label as-is

            elif has_id:
                # Only ID provided: extrapolate label
                assert id_val is not None  # Type narrowing for mypy
                try:
                    enum_member = enum_cls(id_val)
                    data[label_field] = enum_member.label
                except (ValueError, KeyError) as e:
                    raise ValueError(f"Invalid {id_field} value: {id_val}") from e

            elif has_label:
                # Only label provided: extrapolate ID
                try:
                    enum_member = enum_cls(str(label_val))
                    data[id_field] = enum_member.value
                    data[label_field] = enum_member.label  # Canonical casing
                except (ValueError, KeyError):
                    # Unknown label during JSON parsing → map to OTHER (99) if available
                    # This is lenient for untrusted data, unlike direct enum construction
                    if hasattr(enum_cls, "OTHER"):
                        data[id_field] = 99
                        data[label_field] = "Other"  # Use canonical OTHER label
                    else:
                        raise ValueError(
                            f"Unknown {label_field} value: {label_val!r} "
                            f"and {enum_cls.__name__} has no OTHER member"
                        ) from None

        return data
