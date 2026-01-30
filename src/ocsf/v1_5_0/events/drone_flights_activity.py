"""Drone Flights Activity event class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_5_0.objects.enrichment import Enrichment
    from ocsf.v1_5_0.objects.metadata import Metadata
    from ocsf.v1_5_0.objects.network_connection_info import NetworkConnectionInfo
    from ocsf.v1_5_0.objects.network_endpoint import NetworkEndpoint
    from ocsf.v1_5_0.objects.network_proxy import NetworkProxy
    from ocsf.v1_5_0.objects.network_traffic import NetworkTraffic
    from ocsf.v1_5_0.objects.object import Object
    from ocsf.v1_5_0.objects.observable import Observable
    from ocsf.v1_5_0.objects.tls import Tls
    from ocsf.v1_5_0.objects.unmanned_aerial_system import UnmannedAerialSystem
    from ocsf.v1_5_0.objects.unmanned_system_operating_area import UnmannedSystemOperatingArea
    from ocsf.v1_5_0.objects.user import User


class DroneFlightsActivity(OCSFBaseModel):
    """Drone Flights Activity events report the activity of Unmanned Aerial Systems (UAS), their Operators, and mission-planning and authorization metadata as reported by the UAS platforms themselves, by Counter-UAS (CUAS) systems, or other remote monitoring or sensing infrastructure. Based on the Remote ID defined in Standard Specification for Remote ID and Tracking (ASTM Designation: F3411-22a) <a target='_blank' href='https://cdn.standards.iteh.ai/samples/112830/71297057ac42432880a203654f213709/ASTM-F3411-22a.pdf'>ASTM F3411-22a</a>

    OCSF Class UID: 1
    Category:

    See: https://schema.ocsf.io/1.5.0/classes/drone_flights_activity
    """

    # Nested Enums for sibling attribute pairs
    class ActivityId(SiblingEnum):
        """The normalized identifier of the activity that triggered the event.

        OCSF Attribute: activity_id
        """

        UNKNOWN = 0
        CAPTURE = 1
        RECORD = 2
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Capture",
                2: "Record",
                99: "Other",
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
        """The normalized Operational status identifier for the Unmanned Aerial System (UAS).

        OCSF Attribute: status_id
        """

        UNDECLARED = 1
        GROUND = 2
        AIRBORNE = 3
        EMERGENCY = 4
        REMOTE_ID_SYSTEM_FAILURE = 5
        RESERVED = 6

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                1: "Undeclared",
                2: "Ground",
                3: "Airborne",
                4: "Emergency",
                5: "Remote ID System Failure",
                6: "Reserved",
            }

    class AuthProtocolId(SiblingEnum):
        """The normalized identifier of the authentication type used to authorize a flight plan or mission.

        OCSF Attribute: auth_protocol_id
        """

        UNKNOWN = 0
        NONE = 1
        UAS_ID_SIGNATURE = 2
        OPERATOR_ID_SIGNATURE = 3
        MESSAGE_SET_SIGNATURE = 4
        AUTHENTICATION_PROVIDED_BY_NETWORK_REMOTE_ID = 5
        SPECIFIC_AUTHENTICATION_METHOD = 6
        RESERVED = 7
        PRIVATE_USER = 8
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "None",
                2: "UAS ID Signature",
                3: "Operator ID Signature",
                4: "Message Set Signature",
                5: "Authentication Provided by Network Remote ID",
                6: "Specific Authentication Method",
                7: "Reserved",
                8: "Private User",
                99: "Other",
            }

    # Class identifiers
    class_uid: Literal[1] = Field(
        default=1, description="The unique identifier of the event class."
    )
    category_uid: Literal[0] = Field(default=0, description="The category unique identifier.")
    activity_id: ActivityId = Field(
        ..., description="The normalized identifier of the activity that triggered the event."
    )
    dst_endpoint: NetworkEndpoint = Field(
        ...,
        description="The destination network endpoint of the Unmanned Aerial System (UAS), Counter Unmanned Aerial System (CUAS) platform, or other unmanned systems monitoring and/or sensing infrastructure.",
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
    unmanned_aerial_system: UnmannedAerialSystem = Field(
        ...,
        description="The Unmanned Aerial System object describes the characteristics, Position Location Information (PLI), and other metadata of Unmanned Aerial Systems (UAS) and other unmanned and drone systems used in Remote ID. Remote ID is defined in the Standard Specification for Remote ID and Tracking (ASTM Designation: F3411-22a) <a target='_blank' href='https://cdn.standards.iteh.ai/samples/112830/71297057ac42432880a203654f213709/ASTM-F3411-22a.pdf'>ASTM F3411-22a</a>.",
    )
    unmanned_system_operator: User = Field(
        ..., description="The human or machine operator of an Unmanned System."
    )
    activity_name: str | None = Field(
        default=None, description="The event activity name, as defined by the activity_id."
    )
    auth_protocol: str | None = Field(
        default=None,
        description="The authentication type as defined by the caption of <code>auth_protocol_id</code>. In the case of 'Other', it is defined by the event source.",
    )
    auth_protocol_id: AuthProtocolId | None = Field(
        default=None,
        description="The normalized identifier of the authentication type used to authorize a flight plan or mission.",
    )
    category_name: str | None = Field(
        default=None, description="The event category name, as defined by category_uid value."
    )
    class_name: str | None = Field(
        default=None, description="The event class name, as defined by class_uid value."
    )
    classification: str | None = Field(
        default=None,
        description="UA Classification - Allows a region to classify UAS in a regional specific manner. The format may differ from region to region.",
    )
    comment: str | None = Field(
        default=None,
        description="This optional, free-text field enables the operator to describe the purpose of a flight, if so desired.",
    )
    connection_info: NetworkConnectionInfo | None = Field(
        default=None, description="The network connection information. [Recommended]"
    )
    count: int | None = Field(
        default=None,
        description="The number of times that events in the same logical group occurred during the event <strong>Start Time</strong> to <strong>End Time</strong> period.",
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
    protocol_name: str | None = Field(
        default=None,
        description="The networking protocol associated with the Remote ID device or beacon. E.g. <code>BLE</code>, <code>LTE</code>, <code>802.11</code>.",
    )
    proxy_endpoint: NetworkProxy | None = Field(
        default=None, description="The proxy (server) in a network connection. [Recommended]"
    )
    raw_data: str | None = Field(
        default=None, description="The raw event/finding data as received from the source."
    )
    raw_data_size: int | None = Field(
        default=None,
        description="The size of the raw data which was transformed into an OCSF event, in bytes.",
    )
    severity: str | None = Field(
        default=None,
        description="The event/finding severity, normalized to the caption of the <code>severity_id</code> value. In the case of 'Other', it is defined by the source.",
    )
    src_endpoint: NetworkEndpoint | None = Field(
        default=None, description="The network source endpoint."
    )
    start_time: int | None = Field(
        default=None,
        description="The start time of a time period, or the time of the least recent event included in the aggregate event.",
    )
    status: str | None = Field(
        default=None,
        description="The normalized Operational status for the Unmanned Aerial System (UAS) normalized to the caption of the <code>status_id</code> value. In the case of 'Other', it is defined by the source.",
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
        default=None,
        description="The normalized Operational status identifier for the Unmanned Aerial System (UAS). [Recommended]",
    )
    timezone_offset: int | None = Field(
        default=None,
        description="The number of minutes that the reported event <code>time</code> is ahead or behind UTC, in the range -1,080 to +1,080. [Recommended]",
    )
    tls: Tls | None = Field(
        default=None, description="The Transport Layer Security (TLS) attributes."
    )
    traffic: NetworkTraffic | None = Field(
        default=None,
        description="Traffic refers to the amount of data transmitted from a Unmanned Aerial System (UAS) or Counter Unmanned Aerial System (UAS) (CUAS) system at a given point of time. Ex: <code>bytes_in</code> and <code>bytes_out</code>.",
    )
    type_name: str | None = Field(
        default=None, description="The event/finding type name, as defined by the type_uid."
    )
    unmanned_system_operating_area: UnmannedSystemOperatingArea | None = Field(
        default=None,
        description="The UAS Operating Area object describes details about a precise area of operations for a UAS flight or mission. [Recommended]",
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
        """
        if not isinstance(data, dict):
            return data

        # Sibling pairs for this event class
        siblings: list[tuple[str, str, type[SiblingEnum]]] = [
            ("activity_id", "activity_name", cls.ActivityId),
            ("severity_id", "severity", cls.SeverityId),
            ("status_id", "status", cls.StatusId),
            ("auth_protocol_id", "auth_protocol", cls.AuthProtocolId),
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
