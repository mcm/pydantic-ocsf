"""Network Interface object."""

from __future__ import annotations

from typing import Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum


class NetworkInterface(OCSFBaseModel):
    """The Network Interface object describes the type and associated attributes of a network interface.

    See: https://schema.ocsf.io/1.0.0/objects/network_interface
    """

    # Nested Enums for sibling attribute pairs
    class TypeId(SiblingEnum):
        """The network interface type identifier.

        OCSF Attribute: type_id
        """

        UNKNOWN = 0
        WIRED = 1
        WIRELESS = 2
        MOBILE = 3
        TUNNEL = 4
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Wired",
                2: "Wireless",
                3: "Mobile",
                4: "Tunnel",
                99: "Other",
            }

    type_id: TypeId = Field(..., description="The network interface type identifier.")
    hostname: Any | None = Field(
        default=None,
        description="The hostname associated with the network interface. [Recommended]",
    )
    ip: Any | None = Field(
        default=None,
        description="The IP address associated with the network interface. [Recommended]",
    )
    mac: Any | None = Field(
        default=None, description="The MAC address of the network interface. [Recommended]"
    )
    name: str | None = Field(default=None, description="The name of the network interface.")
    namespace: str | None = Field(
        default=None,
        description="The namespace is useful in merger or acquisition situations. For example, when similar entities exists that you need to keep separate.",
    )
    subnet_prefix: int | None = Field(
        default=None,
        description="The subnet prefix length determines the number of bits used to represent the network part of the IP address. The remaining bits are reserved for identifying individual hosts within that subnet.",
    )
    type_: str | None = Field(default=None, description="The type of network interface.")
    uid: str | None = Field(
        default=None, description="The unique identifier for the network interface."
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
