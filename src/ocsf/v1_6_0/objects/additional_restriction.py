"""Additional Restriction object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_6_0.objects.policy import Policy


class AdditionalRestriction(OCSFBaseModel):
    """The Additional Restriction object describes supplementary access controls and guardrails that constrain or limit granted permissions beyond the primary policy. These restrictions are typically applied through hierarchical policy frameworks, organizational controls, or conditional access mechanisms. Examples include AWS Service Control Policies (SCPs), Resource Control Policies (RCPs), Azure Management Group policies, GCP Organization policies, conditional access policies, IP restrictions, time-based constraints, and MFA requirements.

    See: https://schema.ocsf.io/1.6.0/objects/additional_restriction
    """

    # Nested Enums for sibling attribute pairs
    class StatusId(SiblingEnum):
        """The normalized status identifier indicating the applicability of this policy restriction.

        OCSF Attribute: status_id
        """

        APPLICABLE = 1
        INAPPLICABLE = 2
        EVALUATION_ERROR = 3

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                1: "Applicable",
                2: "Inapplicable",
                3: "Evaluation Error",
            }

    policy: Policy = Field(
        ...,
        description="Detailed information about the policy document that defines this restriction, including policy metadata, type, scope, and the specific rules or conditions that implement the access control.",
    )
    status: str | None = Field(
        default=None,
        description="The current status of the policy restriction, normalized to the caption of the <code>status_id</code> enum value.",
    )
    status_id: StatusId | None = Field(
        default=None,
        description="The normalized status identifier indicating the applicability of this policy restriction. [Recommended]",
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
