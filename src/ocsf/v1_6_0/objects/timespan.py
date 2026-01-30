"""Time Span object."""

from __future__ import annotations

from typing import Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum


class Timespan(OCSFBaseModel):
    """The Time Span object represents different time period durations. If a timespan is fractional, i.e. crosses one period, e.g. a week and 3 days, more than one may be populated since each member is of integral type. In that case <code>type_id</code> if present should be set to <code>Other.</code><P>A timespan may also be defined by its time interval boundaries, <code>start_time</code> and <code>end_time</code>.

    See: https://schema.ocsf.io/1.6.0/objects/timespan
    """

    # Nested Enums for sibling attribute pairs
    class TypeId(SiblingEnum):
        """The normalized identifier for the time span duration type.

        OCSF Attribute: type_id
        """

        UNKNOWN = 0
        MILLISECONDS = 1
        SECONDS = 2
        MINUTES = 3
        HOURS = 4
        DAYS = 5
        WEEKS = 6
        MONTHS = 7
        YEARS = 8
        TIME_INTERVAL = 9
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Milliseconds",
                2: "Seconds",
                3: "Minutes",
                4: "Hours",
                5: "Days",
                6: "Weeks",
                7: "Months",
                8: "Years",
                9: "Time Interval",
                99: "Other",
            }

    duration: int | None = Field(
        default=None, description="The duration of the time span in milliseconds. [Recommended]"
    )
    duration_days: int | None = Field(
        default=None, description="The duration of the time span in days. [Recommended]"
    )
    duration_hours: int | None = Field(
        default=None, description="The duration of the time span in hours. [Recommended]"
    )
    duration_mins: int | None = Field(
        default=None, description="The duration of the time span in minutes. [Recommended]"
    )
    duration_months: int | None = Field(
        default=None, description="The duration of the time span in months. [Recommended]"
    )
    duration_secs: int | None = Field(
        default=None, description="The duration of the time span in seconds. [Recommended]"
    )
    duration_weeks: int | None = Field(
        default=None, description="The duration of the time span in weeks. [Recommended]"
    )
    duration_years: int | None = Field(
        default=None, description="The duration of the time span in years. [Recommended]"
    )
    end_time: int | None = Field(
        default=None,
        description="The end time or conclusion of the timespan's interval. [Recommended]",
    )
    start_time: int | None = Field(
        default=None,
        description="The start time or beginning of the timespan's interval. [Recommended]",
    )
    type_: str | None = Field(
        default=None, description="The type of time span duration the object represents."
    )
    type_id: TypeId | None = Field(
        default=None,
        description="The normalized identifier for the time span duration type. [Recommended]",
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
