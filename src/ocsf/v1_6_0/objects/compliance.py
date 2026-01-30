"""Compliance object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_6_0.objects.assessment import Assessment
    from ocsf.v1_6_0.objects.check import Check
    from ocsf.v1_6_0.objects.kb_article import KbArticle
    from ocsf.v1_6_0.objects.key_value_object import KeyValueObject


class Compliance(OCSFBaseModel):
    """The Compliance object contains information about Industry and Regulatory Framework standards, controls and requirements or details about custom assessments utilized in a compliance evaluation. Standards define broad security frameworks, controls represent specific security requirements within those frameworks, and checks are the testable verification points used to determine if controls are properly implemented.

    See: https://schema.ocsf.io/1.6.0/objects/compliance
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

    assessments: list[Assessment] | None = Field(
        default=None,
        description="A list of assessments associated with the compliance requirements evaluation.",
    )
    category: str | None = Field(
        default=None,
        description="The category a control framework pertains to, as reported by the source tool, such as <code>Asset Management</code> or <code>Risk Assessment</code>.",
    )
    checks: list[Check] | None = Field(
        default=None,
        description="A list of compliance checks associated with specific industry standards or frameworks. Each check represents an individual rule or requirement that has been evaluated against a target device. Checks typically include details such as the check name (e.g., CIS: 'Ensure mounting of cramfs filesystems is disabled' or DISA STIG descriptive titles), unique identifiers (such as CIS identifier '1.1.1.1' or DISA STIG identifier 'V-230234'), descriptions (detailed explanations of security requirements or vulnerability discussions), and version information.",
    )
    compliance_references: list[KbArticle] | None = Field(
        default=None,
        description="A list of reference KB articles that provide information to help organizations understand, interpret, and implement compliance standards. They provide guidance, best practices, and examples.",
    )
    compliance_standards: list[KbArticle] | None = Field(
        default=None,
        description="A list of established guidelines or criteria that define specific requirements an organization must follow.",
    )
    control: str | None = Field(
        default=None,
        description="A Control is a prescriptive, actionable set of specifications that strengthens device posture. The control specifies required security measures, while the specific implementation values are defined in control_parameters. E.g., CIS AWS Foundations Benchmark 1.2.0 - Control 2.1 - Ensure CloudTrail is enabled in all regions [Recommended]",
    )
    control_parameters: list[KeyValueObject] | None = Field(
        default=None,
        description="The list of control parameters evaluated in a Compliance check. E.g., parameters for CloudTrail configuration might include <code>multiRegionTrailEnabled: true</code>, <code>logFileValidationEnabled: true</code>, and <code>requiredRegions: [us-east-1, us-west-2]</code>",
    )
    desc: str | None = Field(default=None, description="The description or criteria of a control.")
    requirements: list[str] | None = Field(
        default=None,
        description="The specific compliance requirements being evaluated. E.g., <code>PCI DSS Requirement 8.2.3 - Passwords must meet minimum complexity requirements</code> or <code>HIPAA Security Rule 164.312(a)(2)(iv) - Implement encryption and decryption mechanisms</code>",
    )
    standards: list[str] | None = Field(
        default=None,
        description="The regulatory or industry standards being evaluated for compliance. [Recommended]",
    )
    status: str | None = Field(
        default=None,
        description="The resultant status of the compliance check normalized to the caption of the <code>status_id</code> value. In the case of 'Other', it is defined by the event source. [Recommended]",
    )
    status_code: str | None = Field(
        default=None, description="The resultant status code of the compliance check."
    )
    status_detail: str | None = Field(
        default=None,
        description="The contextual description of the <code>status, status_code</code> values.",
    )
    status_details: list[str] | None = Field(
        default=None,
        description="A list of contextual descriptions of the <code>status, status_code</code> values.",
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
