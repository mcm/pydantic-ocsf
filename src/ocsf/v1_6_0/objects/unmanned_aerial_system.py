"""Unmanned Aerial System object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_6_0.objects.device_hw_info import DeviceHwInfo
    from ocsf.v1_6_0.objects.location import Location


class UnmannedAerialSystem(OCSFBaseModel):
    """The Unmanned Aerial System object describes the characteristics, Position Location Information (PLI), and other metadata of Unmanned Aerial Systems (UAS) and other unmanned and drone systems used in Remote ID. Remote ID is defined in the Standard Specification for Remote ID and Tracking (ASTM Designation: F3411-22a) <a target='_blank' href='https://cdn.standards.iteh.ai/samples/112830/71297057ac42432880a203654f213709/ASTM-F3411-22a.pdf'>ASTM F3411-22a</a>.

    See: https://schema.ocsf.io/1.6.0/objects/unmanned_aerial_system
    """

    # Nested Enums for sibling attribute pairs
    class TypeId(SiblingEnum):
        """The UAS type identifier.

        OCSF Attribute: type_id
        """

        UNKNOWNUNDECLARED = 0
        AIRPLANE = 1
        HELICOPTER = 2
        GYROPLANE = 3
        HYBRID_LIFT = 4
        ORNITHOPTER = 5
        GLIDER = 6
        KITE = 7
        FREE_BALLOON = 8
        CAPTIVE_BALLOON = 9
        AIRSHIP = 10
        FREE_FALLPARACHUTE = 11
        ROCKET = 12
        TETHERED_POWERED_AIRCRAFT = 13
        GROUND_OBSTACLE = 14
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown/Undeclared",
                1: "Airplane",
                2: "Helicopter",
                3: "Gyroplane",
                4: "Hybrid Lift",
                5: "Ornithopter",
                6: "Glider",
                7: "Kite",
                8: "Free Balloon",
                9: "Captive Balloon",
                10: "Airship",
                11: "Free Fall/Parachute",
                12: "Rocket",
                13: "Tethered Powered Aircraft",
                14: "Ground Obstacle",
                99: "Other",
            }

    hw_info: DeviceHwInfo | None = Field(
        default=None, description="The endpoint hardware information."
    )
    location: Location | None = Field(
        default=None,
        description="The detailed geographical location usually associated with an IP address. [Recommended]",
    )
    model: str | None = Field(
        default=None, description="The model name of the aircraft or unmanned system."
    )
    name: str | None = Field(
        default=None,
        description="The name of the unmanned system as reported by tracking or sensing hardware.",
    )
    serial_number: str | None = Field(
        default=None,
        description="The serial number of the unmanned system. This is expressed in <code>CTA-2063-A</code> format. [Recommended]",
    )
    speed: str | None = Field(
        default=None,
        description="Ground speed of flight. This value is provided in meters per second with a minimum resolution of 0.25 m/s. Special Values: <code>Invalid</code>, <code>No Value</code>, or <code>Unknown: 255 m/s</code>.",
    )
    speed_accuracy: str | None = Field(
        default=None,
        description="Provides quality/containment on horizontal ground speed. Measured in meters/second.",
    )
    track_direction: str | None = Field(
        default=None,
        description="Direction of flight expressed as a “True North-based” ground track angle. This value is provided in clockwise degrees with a minimum resolution of 1 degree. If aircraft is not moving horizontally, use the “Unknown” value",
    )
    type_: str | None = Field(
        default=None,
        description="The type of the UAS. For example, Helicopter, Gyroplane, Rocket, etc.",
    )
    type_id: TypeId | None = Field(
        default=None, description="The UAS type identifier. [Recommended]"
    )
    uid: str | None = Field(
        default=None,
        description="The primary identification identifier for an unmanned system. This can be a Serial Number (in <code>CTA-2063-A</code> format, the Registration ID (provided by the <code>CAA</code>, a UTM, or a unique Session ID. [Recommended]",
    )
    uid_alt: str | None = Field(
        default=None,
        description="A secondary identification identifier for an unmanned system. This can be a Serial Number (in <code>CTA-2063-A</code> format, the Registration ID (provided by the <code>CAA</code>, a UTM, or a unique Session ID. [Recommended]",
    )
    uuid: Any | None = Field(
        default=None,
        description="The Unmanned Aircraft System Traffic Management (UTM) provided universal unique ID (UUID) traceable to a non-obfuscated ID where this UTM UUID acts as a 'session id' to protect exposure of operationally sensitive information. [Recommended]",
    )
    vertical_speed: str | None = Field(
        default=None,
        description="Vertical speed upward relative to the WGS-84 datum, measured in meters per second. Special Values: <code>Invalid</code>, <code>No Value</code>, or <code>Unknown: 63 m/s</code>.",
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
