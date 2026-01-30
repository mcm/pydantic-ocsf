"""Check object."""

from __future__ import annotations

from typing import Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum


class Check(OCSFBaseModel):
    """The check object defines a specific, testable compliance verification point that evaluates a target device against a standard, framework, or custom requirement. While checks are typically associated with formal standards (like CIS, NIST, or ISO), they can also represent custom or organizational requirements. When mapped to controls, checks can evaluate specific control_parameters to determine compliance status, but neither the control mapping nor control_parameters are required for a valid check.

    See: https://schema.ocsf.io/1.6.0/objects/check
    """

    # Nested Enums for sibling attribute pairs
    class SeverityId(SiblingEnum):
        """The normalized severity identifier that maps severity levels to standard severity levels. For example CIS Benchmark: <code>Level 2</code> maps to <code>4</code> (High), <code>Level 1</code> maps to <code>3</code> (Medium). For DISA STIG: <code>CAT I</code> maps to <code>5</code> (Critical), <code>CAT II</code> maps to <code>4</code> (High), and <code>CAT III</code> maps to <code>3</code> (Medium).

        OCSF Attribute: severity_id
        """

        UNKNOWN = 0
        INFORMATIONAL = 1
        LOW = 2
        MEDIUM = 3
        HIGH = 4
        CRITICAL = 5
        FATAL = 6
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Informational",
                2: "Low",
                3: "Medium",
                4: "High",
                5: "Critical",
                6: "Fatal",
                99: "Other",
            }

    class StatusId(SiblingEnum):
        """The normalized status identifier of the compliance check.

        OCSF Attribute: status_id
        """

        UNKNOWN = 0
        PASS = 1
        WARNING = 2
        FAIL = 3
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Pass",
                2: "Warning",
                3: "Fail",
                99: "Other",
            }

    desc: str | None = Field(
        default=None,
        description="The detailed description of the compliance check, explaining the security requirement, vulnerability, or configuration being assessed. For example, CIS: <code>The cramfs filesystem type is a compressed read-only Linux filesystem. Removing support for unneeded filesystem types reduces the local attack surface.</code> or DISA STIG: <code>Unauthorized access to the information system by foreign entities may result in loss or compromise of data.</code>",
    )
    name: str | None = Field(
        default=None,
        description="The name or title of the compliance check. For example, CIS: <code>Ensure mounting of cramfs filesystems is disabled</code> or DISA STIG: <code>The Ubuntu operating system must implement DoD-approved encryption to protect the confidentiality of remote access sessions</code>. [Recommended]",
    )
    severity: str | None = Field(
        default=None,
        description="The severity level as defined in the source document. For example CIS Benchmarks, valid values are: <code>Level 1</code> (security-forward, essential settings), <code>Level 2</code> (security-focused environment, more restrictive), or <code>Scored/Not Scored</code> (whether compliance can be automatically checked). For DISA STIG, valid values are: <code>CAT I</code> (maps to severity_id 5/Critical), <code>CAT II</code> (maps to severity_id 4/High), or <code>CAT III</code> (maps to severity_id 3/Medium).",
    )
    severity_id: SeverityId | None = Field(
        default=None,
        description="The normalized severity identifier that maps severity levels to standard severity levels. For example CIS Benchmark: <code>Level 2</code> maps to <code>4</code> (High), <code>Level 1</code> maps to <code>3</code> (Medium). For DISA STIG: <code>CAT I</code> maps to <code>5</code> (Critical), <code>CAT II</code> maps to <code>4</code> (High), and <code>CAT III</code> maps to <code>3</code> (Medium).",
    )
    standards: list[str] | None = Field(
        default=None,
        description="The regulatory or industry standard this check is associated with. E.g., <code>PCI DSS 3.2.1</code>, <code>HIPAA Security Rule</code>, <code>NIST SP 800-53 Rev. 5</code>, or <code>ISO/IEC 27001:2013</code>. [Recommended]",
    )
    status: str | None = Field(
        default=None,
        description="The resultant status of the compliance check normalized to the caption of the <code>status_id</code> value. For example, CIS Benchmark: <code>Pass</code> when all requirements are met, <code>Fail</code> when requirements are not met, or DISA STIG: <code>NotAFinding</code> (maps to status_id 1/Pass), <code>Open</code> (maps to status_id 3/Fail). [Recommended]",
    )
    status_id: StatusId | None = Field(
        default=None,
        description="The normalized status identifier of the compliance check. [Recommended]",
    )
    uid: str | None = Field(
        default=None,
        description="The unique identifier of the compliance check within its standard or framework. For example, CIS Benchmark identifier <code>1.1.1.1</code>, DISA STIG identifier <code>V-230234</code>, or NIST control identifier <code>AC-17(2)</code>. [Recommended]",
    )
    version: str | None = Field(
        default=None,
        description="The check version. For example, CIS Benchmark: <code>1.1.0</code> for Amazon Linux 2 or DISA STIG: <code>V2R1</code> for Windows 10.",
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
            ("severity_id", "severity", cls.SeverityId),
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
