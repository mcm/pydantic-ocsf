"""Unmanned System Operating Area object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_7_0.objects.location import Location


class UnmannedSystemOperatingArea(OCSFBaseModel):
    """The Unmanned System Operating Area object describes details about a precise area of operations for a UAS flight or mission.

    See: https://schema.ocsf.io/1.7.0/objects/unmanned_system_operating_area
    """

    # Nested Enums for sibling attribute pairs
    class TypeId(SiblingEnum):
        """The operating area type identifier.

        OCSF Attribute: type_id
        """

        UNKNOWNUNDECLARED = 0
        TAKEOFF_LOCATION = 1
        FIXED_LOCATION = 2
        DYNAMIC_LOCATION = 3
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown/Undeclared",
                1: "Takeoff Location",
                2: "Fixed Location",
                3: "Dynamic Location",
                99: "Other",
            }

    aerial_height: str | None = Field(
        default=None,
        description="Expressed as either height above takeoff location or height above ground level (AGL) for a UAS current location. This value is provided in meters and must have a minimum resolution of 1 m. Special Values: <code>Invalid</code>, <code>No Value</code>, or <code>Unknown: -1000 m</code>.",
    )
    altitude_ceiling: str | None = Field(
        default=None,
        description="Maximum altitude (WGS-84 HAE) for a group or an Intent-Based Network Participant. Measured in meters. Special Values: <code>Invalid</code>, <code>No Value</code>, or <code>Unknown: -1000 m</code>.",
    )
    altitude_floor: str | None = Field(
        default=None,
        description="Minimum altitude (WGS-84 HAE) for a group or an Intent-Based Network Participant. Measured in meters. Special Values: <code>Invalid</code>, <code>No Value</code>, or <code>Unknown: -1000 m</code>.",
    )
    city: str | None = Field(default=None, description="The name of the city. [Recommended]")
    continent: str | None = Field(
        default=None, description="The name of the continent. [Recommended]"
    )
    coordinates: list[float] | None = Field(
        default=None,
        description="A two-element array, containing a longitude/latitude pair. The format conforms with <a target='_blank' href='https://geojson.org'>GeoJSON</a>. For example: <code>[-73.983, 40.719]</code>.",
    )
    count: int | None = Field(
        default=None, description="Indicates the number of UAS in the operating area. [Recommended]"
    )
    country: str | None = Field(
        default=None,
        description="The ISO 3166-1 Alpha-2 country code.<p><b>Note:</b> The two letter country code should be capitalized. For example: <code>US</code> or <code>CA</code>.</p> [Recommended]",
    )
    desc: str | None = Field(
        default=None, description="The description of the geographical location."
    )
    end_time: int | None = Field(
        default=None,
        description="The date and time at which a group or an Intent-Based Network Participant operation ends. (This field is only applicable to Network Remote ID.)",
    )
    geodetic_altitude: str | None = Field(
        default=None,
        description="The aircraft distance above or below the ellipsoid as measured along a line that passes through the aircraft and is normal to the surface of the WGS-84 ellipsoid. This value is provided in meters and must have a minimum resolution of 1 m. Special Values: <code>Invalid</code>, <code>No Value</code>, or <code>Unknown: -1000 m</code>.",
    )
    geodetic_vertical_accuracy: str | None = Field(
        default=None,
        description="Provides quality/containment on geodetic altitude. This is based on ADS-B Geodetic Vertical Accuracy (GVA). Measured in meters.",
    )
    geohash: str | None = Field(
        default=None,
        description="<p>Geohash of the geo-coordinates (latitude and longitude).</p><a target='_blank' href='https://en.wikipedia.org/wiki/Geohash'>Geohashing</a> is a geocoding system used to encode geographic coordinates in decimal degrees, to a single string.",
    )
    horizontal_accuracy: str | None = Field(
        default=None,
        description="Provides quality/containment on horizontal position. This is based on ADS-B NACp. Measured in meters.",
    )
    is_on_premises: bool | None = Field(
        default=None, description="The indication of whether the location is on premises."
    )
    isp: str | None = Field(
        default=None, description="The name of the Internet Service Provider (ISP)."
    )
    lat: float | None = Field(
        default=None,
        description="The geographical Latitude coordinate represented in Decimal Degrees (DD). For example: <code>42.361145</code>.",
    )
    locations: list[Location] | None = Field(
        default=None,
        description="A list of Position Location Information (PLI) (latitude/longitude pairs) defining the area where a group or Intent-Based Network Participant operation is taking place. (This field is only applicable to Network Remote ID.) [Recommended]",
    )
    long: float | None = Field(
        default=None,
        description="The geographical Longitude coordinate represented in Decimal Degrees (DD). For example: <code>-71.057083</code>.",
    )
    postal_code: str | None = Field(default=None, description="The postal code of the location.")
    pressure_altitude: str | None = Field(
        default=None,
        description="The uncorrected barometric pressure altitude (based on reference standard 29.92 inHg, 1013.25 mb) provides a reference for algorithms that utilize 'altitude deltas' between aircraft. This value is provided in meters and must have a minimum resolution of 1 m.. Special Values: <code>Invalid</code>, <code>No Value</code>, or <code>Unknown: -1000 m</code>.",
    )
    provider: str | None = Field(
        default=None, description="The provider of the geographical location data."
    )
    radius: str | None = Field(
        default=None,
        description="Farthest horizontal distance from the reported location at which any UA in a group may be located (meters). Also allows defining the area where an Intent-Based Network Participant operation is taking place. Default: 0 m.",
    )
    region: str | None = Field(
        default=None,
        description="The alphanumeric code that identifies the principal subdivision (e.g. province or state) of the country. For example, 'CH-VD' for the Canton of Vaud, Switzerland",
    )
    start_time: int | None = Field(
        default=None,
        description="The date and time at which a group or an Intent-Based Network Participant operation starts. (This field is only applicable to Network Remote ID.)",
    )
    type_: str | None = Field(
        default=None,
        description="The type of operating area. For example, <code>Takeoff Location</code>, <code>Fixed Location</code>, <code>Dynamic Location</code>.",
    )
    type_id: TypeId | None = Field(
        default=None, description="The operating area type identifier. [Recommended]"
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
