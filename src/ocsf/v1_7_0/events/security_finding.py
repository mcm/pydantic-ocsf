"""Security Finding event class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_7_0.objects.analytic import Analytic
    from ocsf.v1_7_0.objects.attack import Attack
    from ocsf.v1_7_0.objects.cis_csc import CisCsc
    from ocsf.v1_7_0.objects.compliance import Compliance
    from ocsf.v1_7_0.objects.enrichment import Enrichment
    from ocsf.v1_7_0.objects.finding import Finding
    from ocsf.v1_7_0.objects.fingerprint import Fingerprint
    from ocsf.v1_7_0.objects.kill_chain_phase import KillChainPhase
    from ocsf.v1_7_0.objects.malware import Malware
    from ocsf.v1_7_0.objects.metadata import Metadata
    from ocsf.v1_7_0.objects.object import Object
    from ocsf.v1_7_0.objects.observable import Observable
    from ocsf.v1_7_0.objects.process import Process
    from ocsf.v1_7_0.objects.resource_details import ResourceDetails
    from ocsf.v1_7_0.objects.vulnerability import Vulnerability


class SecurityFinding(OCSFBaseModel):
    """Security Finding events describe findings, detections, anomalies, alerts and/or actions performed by security products

    OCSF Class UID: 1
    Category: findings

    See: https://schema.ocsf.io/1.7.0/classes/security_finding
    """

    # Nested Enums for sibling attribute pairs
    class ActivityId(SiblingEnum):
        """The normalized identifier of the activity that triggered the event.

        OCSF Attribute: activity_id
        """

        CREATE = 1
        UPDATE = 2
        CLOSE = 3

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                1: "Create",
                2: "Update",
                3: "Close",
            }

    class SeverityId(SiblingEnum):
        """<p>The normalized identifier of the event/finding severity.</p>The normalized severity is a measurement the effort and expense required to manage and resolve an event or incident. Smaller numerical values represent lower impact events, and larger numerical values represent higher impact events.

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
        """The normalized identifier of the event status.

        OCSF Attribute: status_id
        """

        UNKNOWN = 0
        SUCCESS = 1
        FAILURE = 2
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Success",
                2: "Failure",
                99: "Other",
            }

    class ConfidenceId(SiblingEnum):
        """The normalized confidence refers to the accuracy of the rule that created the finding. A rule with a low confidence means that the finding scope is wide and may create finding reports that may not be malicious in nature.

        OCSF Attribute: confidence_id
        """

        UNKNOWN = 0
        LOW = 1
        MEDIUM = 2
        HIGH = 3
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Low",
                2: "Medium",
                3: "High",
                99: "Other",
            }

    class ImpactId(SiblingEnum):
        """The normalized impact of the incident or finding. Per NIST, this is the magnitude of harm that can be expected to result from the consequences of unauthorized disclosure, modification, destruction, or loss of information or information system availability.

        OCSF Attribute: impact_id
        """

        UNKNOWN = 0
        LOW = 1
        MEDIUM = 2
        HIGH = 3
        CRITICAL = 4
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Low",
                2: "Medium",
                3: "High",
                4: "Critical",
                99: "Other",
            }

    class RiskLevelId(SiblingEnum):
        """The normalized risk level id.

        OCSF Attribute: risk_level_id
        """

        INFO = 0
        LOW = 1
        MEDIUM = 2
        HIGH = 3
        CRITICAL = 4
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Info",
                1: "Low",
                2: "Medium",
                3: "High",
                4: "Critical",
                99: "Other",
            }

    class StateId(SiblingEnum):
        """The normalized state identifier of a security finding.

        OCSF Attribute: state_id
        """

        NEW = 1
        IN_PROGRESS = 2
        SUPPRESSED = 3
        RESOLVED = 4

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                1: "New",
                2: "In Progress",
                3: "Suppressed",
                4: "Resolved",
            }

    class EventTypeId(SiblingEnum):
        """The event type ID, calculated as class_uid * 100 + activity_id. Identifies the event's semantics and structure.

        OCSF Attribute: type_uid
        """

        CREATE = 101
        UPDATE = 102
        CLOSE = 103

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                101: "Create",
                102: "Update",
                103: "Close",
            }

    # Class identifiers
    class_uid: Literal[1] = Field(
        default=1, description="The unique identifier of the event class."
    )
    category_uid: Literal[0] = Field(default=0, description="The category unique identifier.")
    finding: Finding = Field(
        ...,
        description="The Finding object provides details about a finding/detection generated by a security tool.",
    )
    metadata: Metadata = Field(
        ..., description="The metadata associated with the event or a finding."
    )
    severity_id: SeverityId = Field(
        ...,
        description="<p>The normalized identifier of the event/finding severity.</p>The normalized severity is a measurement the effort and expense required to manage and resolve an event or incident. Smaller numerical values represent lower impact events, and larger numerical values represent higher impact events.",
    )
    state_id: StateId = Field(
        ..., description="The normalized state identifier of a security finding."
    )
    time: int = Field(
        ..., description="The normalized event occurrence time or the finding creation time."
    )
    type_uid: int | None = Field(
        default=None,
        description="The event/finding type ID. It identifies the event's semantics and structure. The value is calculated by the logging system as: <code>class_uid * 100 + activity_id</code>.",
    )
    activity_id: ActivityId | None = Field(
        default=None,
        description="The normalized identifier of the activity that triggered the event.",
    )
    activity_name: str | None = Field(
        default=None, description="The event activity name, as defined by the activity_id."
    )
    analytic: Analytic | None = Field(
        default=None,
        description="The analytic technique used to analyze and derive insights from the data or information that led to the finding or conclusion. [Recommended]",
    )
    attacks: list[Attack] | None = Field(
        default=None,
        description="An array of <a target='_blank' href='https://attack.mitre.org'>MITRE ATT&CK®</a> objects describing the tactics, techniques & sub-techniques associated to the Finding.",
    )
    category_name: str | None = Field(
        default=None, description="The event category name, as defined by category_uid value."
    )
    cis_csc: list[CisCsc] | None = Field(
        default=None,
        description="The CIS Critical Security Controls is a list of top 20 actions and practices an organization’s security team can take on such that cyber attacks or malware, are minimized and prevented.",
    )
    class_name: str | None = Field(
        default=None, description="The event class name, as defined by class_uid value."
    )
    compliance: Compliance | None = Field(
        default=None,
        description="The compliance object provides context to compliance findings (e.g., a check against a specific regulatory or best practice framework such as CIS, NIST etc.) and contains compliance related details.",
    )
    confidence: str | None = Field(
        default=None,
        description="The confidence, normalized to the caption of the confidence_id value. In the case of 'Other', it is defined by the event source. [Recommended]",
    )
    confidence_id: ConfidenceId | None = Field(
        default=None,
        description="The normalized confidence refers to the accuracy of the rule that created the finding. A rule with a low confidence means that the finding scope is wide and may create finding reports that may not be malicious in nature. [Recommended]",
    )
    confidence_score: int | None = Field(
        default=None,
        description="The confidence score as reported by the event source. [Recommended]",
    )
    count: int | None = Field(
        default=None,
        description="The number of times that events in the same logical group occurred during the event <strong>Start Time</strong> to <strong>End Time</strong> period.",
    )
    data_sources: list[str] | None = Field(
        default=None, description="A list of data sources utilized in generation of the finding."
    )
    duration: int | None = Field(
        default=None,
        description="The event duration or aggregate time, the amount of time the event covers from <code>start_time</code> to <code>end_time</code> in milliseconds.",
    )
    end_time: int | None = Field(
        default=None,
        description="The end time of a time period, or the time of the most recent event included in the aggregate event.",
    )
    enrichments: list[Enrichment] | None = Field(
        default=None,
        description='The additional information from an external data source, which is associated with the event or a finding. For example add location information for the IP address in the DNS answers:</p><code>[{"name": "answers.ip", "value": "92.24.47.250", "type": "location", "data": {"city": "Socotra", "continent": "Asia", "coordinates": [-25.4153, 17.0743], "country": "YE", "desc": "Yemen"}}]</code>',
    )
    evidence: dict[str, Any] | None = Field(
        default=None, description="The data the finding exposes to the analyst."
    )
    impact: str | None = Field(
        default=None,
        description="The impact , normalized to the caption of the impact_id value. In the case of 'Other', it is defined by the event source. [Recommended]",
    )
    impact_id: ImpactId | None = Field(
        default=None,
        description="The normalized impact of the incident or finding. Per NIST, this is the magnitude of harm that can be expected to result from the consequences of unauthorized disclosure, modification, destruction, or loss of information or information system availability. [Recommended]",
    )
    impact_score: int | None = Field(
        default=None,
        description="The impact as an integer value of the finding, valid range 0-100. [Recommended]",
    )
    include: str | None = Field(default=None, description="")
    kill_chain: list[KillChainPhase] | None = Field(
        default=None,
        description="The <a target='_blank' href='https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html'>Cyber Kill Chain®</a> provides a detailed description of each phase and its associated activities within the broader context of a cyber attack.",
    )
    malware: list[Malware] | None = Field(
        default=None,
        description="A list of Malware objects, describing details about the identified malware.",
    )
    message: str | None = Field(
        default=None,
        description="The description of the event/finding, as defined by the source. [Recommended]",
    )
    nist: list[str] | None = Field(
        default=None,
        description="The NIST Cybersecurity Framework recommendations for managing the cybersecurity risk.",
    )
    observables: list[Observable] | None = Field(
        default=None,
        description="The observables associated with the event or a finding. [Recommended]",
    )
    process: Process | None = Field(default=None, description="The process object.")
    raw_data: str | None = Field(
        default=None, description="The raw event/finding data as received from the source."
    )
    raw_data_hash: Fingerprint | None = Field(
        default=None, description="The hash, which describes the content of the raw_data field."
    )
    raw_data_size: int | None = Field(
        default=None,
        description="The size of the raw data which was transformed into an OCSF event, in bytes.",
    )
    resources: list[ResourceDetails] | None = Field(
        default=None,
        description="Describes details about resources that were affected by the activity/event. [Recommended]",
    )
    risk_level: str | None = Field(
        default=None,
        description="The risk level, normalized to the caption of the risk_level_id value. [Recommended]",
    )
    risk_level_id: RiskLevelId | None = Field(
        default=None, description="The normalized risk level id. [Recommended]"
    )
    risk_score: int | None = Field(
        default=None, description="The risk score as reported by the event source. [Recommended]"
    )
    severity: str | None = Field(
        default=None,
        description="The event/finding severity, normalized to the caption of the <code>severity_id</code> value. In the case of 'Other', it is defined by the source.",
    )
    start_time: int | None = Field(
        default=None,
        description="The start time of a time period, or the time of the least recent event included in the aggregate event.",
    )
    state: str | None = Field(
        default=None, description="The normalized state of a security finding."
    )
    status: str | None = Field(
        default=None,
        description="The event status, normalized to the caption of the status_id value. In the case of 'Other', it is defined by the event source. [Recommended]",
    )
    status_code: str | None = Field(
        default=None,
        description="The event status code, as reported by the event source.<br /><br />For example, in a Windows Failed Authentication event, this would be the value of 'Failure Code', e.g. 0x18. [Recommended]",
    )
    status_detail: str | None = Field(
        default=None,
        description="The status detail contains additional information about the event/finding outcome. [Recommended]",
    )
    status_id: StatusId | None = Field(
        default=None, description="The normalized identifier of the event status. [Recommended]"
    )
    timezone_offset: int | None = Field(
        default=None,
        description="The number of minutes that the reported event <code>time</code> is ahead or behind UTC, in the range -1,080 to +1,080. [Recommended]",
    )
    type_name: str | None = Field(
        default=None, description="The event/finding type name, as defined by the type_uid."
    )
    unmapped: Object | None = Field(
        default=None,
        description="The attributes that are not mapped to the event schema. The names and values of those attributes are specific to the event source.",
    )
    vulnerabilities: list[Vulnerability] | None = Field(
        default=None,
        description="This object describes vulnerabilities reported in a security finding.",
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

        Special handling for type_uid:
        - Auto-calculated as class_uid * 100 + activity_id if not provided
        - Validated against activity_id if both provided
        """
        if not isinstance(data, dict):
            return data

        # Sibling pairs for this event class
        # Separate type_uid from other siblings (it needs special handling)
        regular_siblings: list[tuple[str, str, type[SiblingEnum]]] = [
            ("activity_id", "activity_name", cls.ActivityId),
            ("severity_id", "severity", cls.SeverityId),
            ("status_id", "status", cls.StatusId),
            ("confidence_id", "confidence", cls.ConfidenceId),
            ("impact_id", "impact", cls.ImpactId),
            ("risk_level_id", "risk_level", cls.RiskLevelId),
            ("state_id", "state", cls.StateId),
        ]

        # First, reconcile regular siblings (this ensures activity_id is available)
        for id_field, label_field, enum_cls in regular_siblings:
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

        # Now handle type_uid - auto-calculate from activity_id
        # (activity_id should be available now after regular sibling reconciliation)
        activity_id = data.get("activity_id")
        type_uid = data.get("type_uid")

        if activity_id is not None and type_uid is None:
            # Auto-calculate type_uid from activity_id
            data["type_uid"] = 1 * 100 + activity_id

        elif activity_id is not None and type_uid is not None:
            # Validate type_uid matches activity_id
            expected_type_uid = 1 * 100 + activity_id
            if type_uid != expected_type_uid:
                raise ValueError(
                    f"type_uid={type_uid} does not match calculated value "
                    f"(class_uid * 100 + activity_id = 1 * 100 + {activity_id} = {expected_type_uid})"
                )

        # Now reconcile type_uid/type_name sibling pair
        id_field, label_field, enum_cls = "type_uid", "type_name", cls.EventTypeId
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
