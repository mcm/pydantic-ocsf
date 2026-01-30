"""Ticket object."""

from __future__ import annotations

from typing import Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum


class Ticket(OCSFBaseModel):
    """The Ticket object represents ticket in the customer's IT Service Management (ITSM) systems like ServiceNow, Jira, etc.

    See: https://schema.ocsf.io/1.7.0/objects/ticket
    """

    # Nested Enums for sibling attribute pairs
    class StatusId(SiblingEnum):
        """The normalized identifier for the ticket status.

        OCSF Attribute: status_id
        """

        NEW = 1
        IN_PROGRESS = 2
        NOTIFIED = 3
        ON_HOLD = 4
        RESOLVED = 5
        CLOSED = 6
        CANCELED = 7
        REOPENED = 8

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                1: "New",
                2: "In Progress",
                3: "Notified",
                4: "On Hold",
                5: "Resolved",
                6: "Closed",
                7: "Canceled",
                8: "Reopened",
            }

    class TypeId(SiblingEnum):
        """The normalized identifier for the ticket type.

        OCSF Attribute: type_id
        """

        UNKNOWN = 0
        INTERNAL = 1
        EXTERNAL = 2
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Internal",
                2: "External",
                99: "Other",
            }

    src_url: Any | None = Field(
        default=None, description="The url of a ticket in the ticket system. [Recommended]"
    )
    status: str | None = Field(
        default=None,
        description="The status of the ticket normalized to the caption of the <code>status_id</code> value. In the case of <code>99</code>, this value should as defined by the source.",
    )
    status_details: list[str] | None = Field(
        default=None,
        description="A list of contextual descriptions of the <code>status, status_id</code> values.",
    )
    status_id: StatusId | None = Field(
        default=None, description="The normalized identifier for the ticket status."
    )
    title: str | None = Field(default=None, description="The title of the ticket.")
    type_: str | None = Field(
        default=None,
        description="The linked ticket type determines whether the ticket is internal or in an external ticketing system.",
    )
    type_id: TypeId | None = Field(
        default=None, description="The normalized identifier for the ticket type."
    )
    uid: str | None = Field(
        default=None, description="Unique identifier of the ticket. [Recommended]"
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
            ("status_id", "status", cls.StatusId),
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
