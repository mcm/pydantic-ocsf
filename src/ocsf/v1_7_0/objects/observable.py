"""Observable object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_7_0.objects.reputation import Reputation


class Observable(OCSFBaseModel):
    """The observable object is a pivot element that contains related information found in many places in the event.

    See: https://schema.ocsf.io/1.7.0/objects/observable
    """

    # Nested Enums for sibling attribute pairs
    class TypeId(SiblingEnum):
        """The observable value type identifier.

        OCSF Attribute: type_id
        """

        UNKNOWN = 0
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                99: "Other",
            }

    type_id: TypeId = Field(..., description="The observable value type identifier.")
    event_uid: str | None = Field(
        default=None,
        description="The unique identifier (<code>metadata.uid</code>) of the source OCSF event from which this observable was extracted. This field enables linking observables back to their originating event data when observables are stored in a separate location or system.",
    )
    name: str | None = Field(
        default=None,
        description="The full name of the observable attribute. The <code>name</code> is a pointer/reference to an attribute within the OCSF event data. For example: <code>file.name</code>. Array attributes may be represented in one of three ways. For example: <code>resources.uid</code>, <code>resources[].uid</code>, <code>resources[0].uid</code>. [Recommended]",
    )
    reputation: Reputation | None = Field(
        default=None, description="Contains the original and normalized reputation scores."
    )
    type_: str | None = Field(default=None, description="The observable value type name.")
    type_uid: int | None = Field(
        default=None,
        description="The OCSF event type UID (<code>type_uid</code>) of the source event that this observable was extracted from. This field enables filtering and categorizing observables by their originating event type. For example: <code>300101</code> for Network Activity (class_uid 3001) with activity_id 1.",
    )
    value: str | None = Field(
        default=None,
        description="The value associated with the observable attribute. The meaning of the value depends on the observable type.<br/>If the <code>name</code> refers to a scalar attribute, then the <code>value</code> is the value of the attribute.<br/>If the <code>name</code> refers to an object attribute, then the <code>value</code> is not populated.",
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
