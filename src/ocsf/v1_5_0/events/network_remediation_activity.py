"""Network Remediation Activity event class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_5_0.objects.d3fend import D3fend
    from ocsf.v1_5_0.objects.enrichment import Enrichment
    from ocsf.v1_5_0.objects.metadata import Metadata
    from ocsf.v1_5_0.objects.network_connection_info import NetworkConnectionInfo
    from ocsf.v1_5_0.objects.object import Object
    from ocsf.v1_5_0.objects.observable import Observable
    from ocsf.v1_5_0.objects.remediation import Remediation
    from ocsf.v1_5_0.objects.scan import Scan


class NetworkRemediationActivity(OCSFBaseModel):
    """Network Remediation Activity events report on attempts at remediating computer networks. It follows the MITRE countermeasures defined by the D3FEND™ <a target='_blank' href='https://d3fend.mitre.org/'>Matrix</a>. Techniques and Sub-techniques will include Network, such as Network Isolation or Network Traffic Filtering.

    OCSF Class UID: 4
    Category:

    See: https://schema.ocsf.io/1.5.0/classes/network_remediation_activity
    """

    # Nested Enums for sibling attribute pairs
    class ActivityId(SiblingEnum):
        """Matches the MITRE D3FEND™ Tactic. Note: the Model and Detect Tactics are not supported as remediations by the OCSF Remediation event class.

        OCSF Attribute: activity_id
        """

        ISOLATE = 1
        EVICT = 2
        RESTORE = 3
        HARDEN = 4
        DETECT = 5

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                1: "Isolate",
                2: "Evict",
                3: "Restore",
                4: "Harden",
                5: "Detect",
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

        DOES_NOT_EXIST = 3
        PARTIAL = 4
        UNSUPPORTED = 5
        ERROR = 6

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                3: "Does Not Exist",
                4: "Partial",
                5: "Unsupported",
                6: "Error",
            }

    class EventTypeId(SiblingEnum):
        """The event type ID, calculated as class_uid * 100 + activity_id. Identifies the event's semantics and structure.

        OCSF Attribute: type_uid
        """

        ISOLATE = 401
        EVICT = 402
        RESTORE = 403
        HARDEN = 404
        DETECT = 405

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                401: "Isolate",
                402: "Evict",
                403: "Restore",
                404: "Harden",
                405: "Detect",
            }

    # Class identifiers
    class_uid: Literal[4] = Field(
        default=4, description="The unique identifier of the event class."
    )
    category_uid: Literal[0] = Field(default=0, description="The category unique identifier.")
    command_uid: str = Field(
        ...,
        description="The unique identifier of the remediation command that pertains to this event.",
    )
    connection_info: NetworkConnectionInfo = Field(
        ..., description="The network connection that pertains to the remediation event."
    )
    metadata: Metadata = Field(
        ..., description="The metadata associated with the event or a finding."
    )
    severity_id: SeverityId = Field(
        ...,
        description="<p>The normalized identifier of the event/finding severity.</p>The normalized severity is a measurement the effort and expense required to manage and resolve an event or incident. Smaller numerical values represent lower impact events, and larger numerical values represent higher impact events.",
    )
    time: int = Field(
        ..., description="The normalized event occurrence time or the finding creation time."
    )
    type_uid: int = Field(
        ...,
        description="The event/finding type ID. It identifies the event's semantics and structure. The value is calculated by the logging system as: <code>class_uid * 100 + activity_id</code>.",
    )
    activity_id: ActivityId | None = Field(
        default=None,
        description="Matches the MITRE D3FEND™ Tactic. Note: the Model and Detect Tactics are not supported as remediations by the OCSF Remediation event class.",
    )
    activity_name: str | None = Field(
        default=None, description="The event activity name, as defined by the activity_id."
    )
    category_name: str | None = Field(
        default=None, description="The event category name, as defined by category_uid value."
    )
    class_name: str | None = Field(
        default=None, description="The event class name, as defined by class_uid value."
    )
    count: int | None = Field(
        default=None,
        description="The number of times that events in the same logical group occurred during the event <strong>Start Time</strong> to <strong>End Time</strong> period.",
    )
    countermeasures: list[D3fend] | None = Field(
        default=None,
        description="The MITRE D3FEND™ Matrix Countermeasures associated with a remediation. [Recommended]",
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
    include: str | None = Field(default=None, description="")
    message: str | None = Field(
        default=None,
        description="The description of the event/finding, as defined by the source. [Recommended]",
    )
    observables: list[Observable] | None = Field(
        default=None,
        description="The observables associated with the event or a finding. [Recommended]",
    )
    raw_data: str | None = Field(
        default=None, description="The raw event/finding data as received from the source."
    )
    raw_data_size: int | None = Field(
        default=None,
        description="The size of the raw data which was transformed into an OCSF event, in bytes.",
    )
    remediation: Remediation | None = Field(
        default=None,
        description="Describes the recommended remediation steps to address identified issue(s).",
    )
    scan: Scan | None = Field(
        default=None, description="The remediation scan that pertains to this event."
    )
    severity: str | None = Field(
        default=None,
        description="The event/finding severity, normalized to the caption of the <code>severity_id</code> value. In the case of 'Other', it is defined by the source.",
    )
    start_time: int | None = Field(
        default=None,
        description="The start time of a time period, or the time of the least recent event included in the aggregate event.",
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
        default=None, description="The normalized identifier of the event status."
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
        ]

        # First, reconcile regular siblings (this ensures activity_id is available)
        for id_field, label_field, enum_cls in regular_siblings:
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

        # Now handle type_uid - auto-calculate from activity_id
        # (activity_id should be available now after regular sibling reconciliation)
        activity_id = data.get("activity_id")
        type_uid = data.get("type_uid")

        if activity_id is not None and type_uid is None:
            # Auto-calculate type_uid from activity_id
            data["type_uid"] = 4 * 100 + activity_id

        elif activity_id is not None and type_uid is not None:
            # Validate type_uid matches activity_id
            expected_type_uid = 4 * 100 + activity_id
            if type_uid != expected_type_uid:
                raise ValueError(
                    f"type_uid={type_uid} does not match calculated value "
                    f"(class_uid * 100 + activity_id = 4 * 100 + {activity_id} = {expected_type_uid})"
                )

        # Now reconcile type_uid/type_name sibling pair
        id_field, label_field, enum_cls = "type_uid", "type_name", cls.EventTypeId
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
