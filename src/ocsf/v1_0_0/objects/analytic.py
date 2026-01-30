"""Analytic object."""

from __future__ import annotations

from typing import Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum


class Analytic(OCSFBaseModel):
    """The Analytic object contains details about the analytic technique used to analyze and derive insights from the data or information that led to the finding or conclusion.

    See: https://schema.ocsf.io/1.0.0/objects/analytic
    """

    # Nested Enums for sibling attribute pairs
    class TypeId(SiblingEnum):
        """The analytic type ID.

        OCSF Attribute: type_id
        """

        UNKNOWN = 0
        RULE = 1
        BEHAVIORAL = 2
        STATISTICAL = 3
        LEARNING_MLDL = 4
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Rule",
                2: "Behavioral",
                3: "Statistical",
                4: "Learning (ML/DL)",
                99: "Other",
            }

    name: str = Field(..., description="The name of the analytic that generated the finding.")
    type_id: TypeId = Field(..., description="The analytic type ID.")
    category: str | None = Field(default=None, description="The analytic category.")
    desc: str | None = Field(
        default=None, description="The description of the analytic that generated the finding."
    )
    related_analytics: list[Analytic] | None = Field(
        default=None,
        description="Describes analytics related to the analytic of a finding or detection as identified by the security product.",
    )
    type_: str | None = Field(default=None, description="The analytic type.")
    uid: str | None = Field(
        default=None,
        description="The unique identifier of the analytic that generated the finding. [Recommended]",
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
