"""Analytic object."""

from __future__ import annotations

from typing import Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum


class Analytic(OCSFBaseModel):
    """The Analytic object contains details about the analytic technique used to analyze and derive insights from the data or information that led to the creation of a finding or conclusion.

    See: https://schema.ocsf.io/1.7.0/objects/analytic
    """

    # Nested Enums for sibling attribute pairs
    class StateId(SiblingEnum):
        """The Analytic state identifier.

        OCSF Attribute: state_id
        """

        ACTIVE = 1
        SUPPRESSED = 2
        EXPERIMENTAL = 3

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                1: "Active",
                2: "Suppressed",
                3: "Experimental",
            }

    class TypeId(SiblingEnum):
        """The analytic type ID.

        OCSF Attribute: type_id
        """

        UNKNOWN = 0
        RULE = 1
        BEHAVIORAL = 2
        STATISTICAL = 3
        LEARNING_MLDL = 4
        FINGERPRINTING = 5
        TAGGING = 6
        KEYWORD_MATCH = 7
        REGULAR_EXPRESSIONS = 8
        EXACT_DATA_MATCH = 9
        PARTIAL_DATA_MATCH = 10
        INDEXED_DATA_MATCH = 11
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Rule",
                2: "Behavioral",
                3: "Statistical",
                4: "Learning (ML/DL)",
                5: "Fingerprinting",
                6: "Tagging",
                7: "Keyword Match",
                8: "Regular Expressions",
                9: "Exact Data Match",
                10: "Partial Data Match",
                11: "Indexed Data Match",
                99: "Other",
            }

    type_id: TypeId = Field(..., description="The analytic type ID.")
    algorithm: str | None = Field(
        default=None,
        description="The algorithm used by the underlying analytic to generate the finding.",
    )
    category: str | None = Field(default=None, description="The analytic category.")
    desc: str | None = Field(
        default=None, description="The description of the analytic that generated the finding."
    )
    name: str | None = Field(
        default=None, description="The name of the analytic that generated the finding."
    )
    related_analytics: list[Analytic] | None = Field(
        default=None, description="Other analytics related to this analytic."
    )
    state: str | None = Field(default=None, description="The Analytic state.")
    state_id: StateId | None = Field(default=None, description="The Analytic state identifier.")
    type_: str | None = Field(default=None, description="The analytic type.")
    uid: str | None = Field(
        default=None,
        description="The unique identifier of the analytic that generated the finding.",
    )
    version: str | None = Field(
        default=None, description="The analytic version. For example: <code>1.1</code>."
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
            ("state_id", "state", cls.StateId),
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
