"""Compliance object."""

from __future__ import annotations

from typing import Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum


class Compliance(OCSFBaseModel):
    """The Compliance object contains information about Industry and Regulatory Framework standards, controls and requirements.

    See: https://schema.ocsf.io/1.1.0/objects/compliance
    """

    # Nested Enums for sibling attribute pairs
    class StatusId(SiblingEnum):
        """The normalized status identifier of the compliance check.

        OCSF Attribute: status_id
        """

        PASS = 1
        WARNING = 2
        FAIL = 3

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                1: "Pass",
                2: "Warning",
                3: "Fail",
            }

    standards: list[str] = Field(
        ...,
        description="Security standards are a set of criteria organizations can follow to protect sensitive and confidential information. e.g. <code>NIST SP 800-53, CIS AWS Foundations Benchmark v1.4.0, ISO/IEC 27001</code>",
    )
    control: str | None = Field(
        default=None,
        description="A Control is prescriptive, prioritized, and simplified set of best practices that one can use to strengthen their cybersecurity posture. e.g. AWS SecurityHub Controls, CIS Controls. [Recommended]",
    )
    requirements: list[str] | None = Field(
        default=None,
        description="A list of requirements associated to a specific control in an industry or regulatory framework. e.g. <code> NIST.800-53.r5 AU-10 </code>",
    )
    status: str | None = Field(
        default=None,
        description="The resultant status of the compliance check  normalized to the caption of the <code>status_id</code> value. In the case of 'Other', it is defined by the event source. [Recommended]",
    )
    status_code: str | None = Field(
        default=None, description="The resultant status code of the compliance check."
    )
    status_detail: str | None = Field(
        default=None, description="The contextual description of the status, status_code values."
    )
    status_id: StatusId | None = Field(
        default=None,
        description="The normalized status identifier of the compliance check. [Recommended]",
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
