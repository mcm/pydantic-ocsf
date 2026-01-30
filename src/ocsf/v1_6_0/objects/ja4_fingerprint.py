"""JA4+ Fingerprint object."""

from __future__ import annotations

from typing import Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum


class Ja4Fingerprint(OCSFBaseModel):
    """The JA4+ fingerprint object provides detailed fingerprint information about various aspects of network traffic which is both machine and human readable.

    See: https://schema.ocsf.io/1.6.0/objects/ja4_fingerprint
    """

    # Nested Enums for sibling attribute pairs
    class TypeId(SiblingEnum):
        """The identifier of the JA4+ fingerprint type.

        OCSF Attribute: type_id
        """

        UNKNOWN = 0
        JA4 = 1
        JA4SERVER = 2
        JA4HTTP = 3
        JA4LATENCY = 4
        JA4X509 = 5
        JA4SSH = 6
        JA4TCP = 7
        JA4TCPSERVER = 8
        JA4TCPSCAN = 9
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "JA4",
                2: "JA4Server",
                3: "JA4HTTP",
                4: "JA4Latency",
                5: "JA4X509",
                6: "JA4SSH",
                7: "JA4TCP",
                8: "JA4TCPServer",
                9: "JA4TCPScan",
                99: "Other",
            }

    type_id: TypeId = Field(..., description="The identifier of the JA4+ fingerprint type.")
    value: str = Field(..., description="The JA4+ fingerprint value.")
    section_a: str | None = Field(
        default=None, description="The 'a' section of the JA4 fingerprint."
    )
    section_b: str | None = Field(
        default=None, description="The 'b' section of the JA4 fingerprint."
    )
    section_c: str | None = Field(
        default=None, description="The 'c' section of the JA4 fingerprint."
    )
    section_d: str | None = Field(
        default=None, description="The 'd' section of the JA4 fingerprint."
    )
    type_: str | None = Field(
        default=None,
        description="The JA4+ fingerprint type as defined by <a href='https://blog.foxio.io/ja4+-network-fingerprinting target='_blank'>FoxIO</a>, normalized to the caption of 'type_id'. In the case of 'Other', it is defined by the event source.",
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
