"""File Hosting Activity event class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_6_0.objects.actor import Actor
    from ocsf.v1_6_0.objects.enrichment import Enrichment
    from ocsf.v1_6_0.objects.file import File
    from ocsf.v1_6_0.objects.fingerprint import Fingerprint
    from ocsf.v1_6_0.objects.http_request import HttpRequest
    from ocsf.v1_6_0.objects.http_response import HttpResponse
    from ocsf.v1_6_0.objects.metadata import Metadata
    from ocsf.v1_6_0.objects.network_connection_info import NetworkConnectionInfo
    from ocsf.v1_6_0.objects.network_endpoint import NetworkEndpoint
    from ocsf.v1_6_0.objects.object import Object
    from ocsf.v1_6_0.objects.observable import Observable


class FileHosting(OCSFBaseModel):
    """File Hosting Activity events report the actions taken by file management applications, including file sharing servers like Sharepoint and services such as Box, MS OneDrive, Google Drive, or network file share services.

    OCSF Class UID: 6
    Category:

    See: https://schema.ocsf.io/1.6.0/classes/file_hosting
    """

    # Nested Enums for sibling attribute pairs
    class ActivityId(SiblingEnum):
        """The normalized identifier of the activity that triggered the event.

        OCSF Attribute: activity_id
        """

        UPLOAD = 1
        DOWNLOAD = 2
        UPDATE = 3
        DELETE = 4
        RENAME = 5
        COPY = 6
        MOVE = 7
        RESTORE = 8
        PREVIEW = 9
        LOCK = 10
        UNLOCK = 11
        SHARE = 12
        UNSHARE = 13
        OPEN = 14
        SYNC = 15
        UNSYNC = 16
        ACCESS_CHECK = 17

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                1: "Upload",
                2: "Download",
                3: "Update",
                4: "Delete",
                5: "Rename",
                6: "Copy",
                7: "Move",
                8: "Restore",
                9: "Preview",
                10: "Lock",
                11: "Unlock",
                12: "Share",
                13: "Unshare",
                14: "Open",
                15: "Sync",
                16: "Unsync",
                17: "Access Check",
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

    class ShareTypeId(SiblingEnum):
        """The normalized identifier of the share type.

        OCSF Attribute: share_type_id
        """

        UNKNOWN = 0
        FILE = 1
        PIPE = 2
        PRINT = 3
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "File",
                2: "Pipe",
                3: "Print",
                99: "Other",
            }

    class EventTypeId(SiblingEnum):
        """The event type ID, calculated as class_uid * 100 + activity_id. Identifies the event's semantics and structure.

        OCSF Attribute: type_uid
        """

        UPLOAD = 601
        DOWNLOAD = 602
        UPDATE = 603
        DELETE = 604
        RENAME = 605
        COPY = 606
        MOVE = 607
        RESTORE = 608
        PREVIEW = 609
        LOCK = 610
        UNLOCK = 611
        SHARE = 612
        UNSHARE = 613
        OPEN = 614
        SYNC = 615
        UNSYNC = 616
        ACCESS_CHECK = 617

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                601: "Upload",
                602: "Download",
                603: "Update",
                604: "Delete",
                605: "Rename",
                606: "Copy",
                607: "Move",
                608: "Restore",
                609: "Preview",
                610: "Lock",
                611: "Unlock",
                612: "Share",
                613: "Unshare",
                614: "Open",
                615: "Sync",
                616: "Unsync",
                617: "Access Check",
            }

    # Class identifiers
    class_uid: Literal[6] = Field(
        default=6, description="The unique identifier of the event class."
    )
    category_uid: Literal[0] = Field(default=0, description="The category unique identifier.")
    actor: Actor = Field(
        ..., description="The actor that performed the activity on the target file."
    )
    file: File = Field(..., description="The file that is the target of the activity.")
    metadata: Metadata = Field(
        ..., description="The metadata associated with the event or a finding."
    )
    severity_id: SeverityId = Field(
        ...,
        description="<p>The normalized identifier of the event/finding severity.</p>The normalized severity is a measurement the effort and expense required to manage and resolve an event or incident. Smaller numerical values represent lower impact events, and larger numerical values represent higher impact events.",
    )
    src_endpoint: NetworkEndpoint = Field(
        ..., description="The endpoint that performed the activity on the target file."
    )
    time: int = Field(
        ..., description="The normalized event occurrence time or the finding creation time."
    )
    type_uid: int | None = Field(
        default=None,
        description="The event/finding type ID. It identifies the event's semantics and structure. The value is calculated by the logging system as: <code>class_uid * 100 + activity_id</code>.",
    )
    access_list: list[str] | None = Field(
        default=None, description="The list of requested access rights."
    )
    access_mask: int | None = Field(
        default=None, description="The sum of hexadecimal values of requested access rights."
    )
    access_result: dict[str, Any] | None = Field(
        default=None, description="The list of access check results."
    )
    activity_id: ActivityId | None = Field(
        default=None,
        description="The normalized identifier of the activity that triggered the event.",
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
    connection_info: NetworkConnectionInfo | None = Field(
        default=None, description="The network connection information."
    )
    count: int | None = Field(
        default=None,
        description="The number of times that events in the same logical group occurred during the event <strong>Start Time</strong> to <strong>End Time</strong> period.",
    )
    dst_endpoint: NetworkEndpoint | None = Field(
        default=None,
        description="The endpoint that received the activity on the target file. [Recommended]",
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
    expiration_time: int | None = Field(default=None, description="The share expiration time.")
    file_result: File | None = Field(
        default=None,
        description="The resulting file object when the activity was allowed and successful.",
    )
    http_request: HttpRequest | None = Field(
        default=None, description="Details about the underlying HTTP request. [Recommended]"
    )
    http_response: HttpResponse | None = Field(
        default=None, description="Details about the HTTP response, if available."
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
    raw_data_hash: Fingerprint | None = Field(
        default=None, description="The hash, which describes the content of the raw_data field."
    )
    raw_data_size: int | None = Field(
        default=None,
        description="The size of the raw data which was transformed into an OCSF event, in bytes.",
    )
    severity: str | None = Field(
        default=None,
        description="The event/finding severity, normalized to the caption of the <code>severity_id</code> value. In the case of 'Other', it is defined by the source.",
    )
    share: str | None = Field(default=None, description="The share name.")
    share_type: str | None = Field(
        default=None,
        description="The share type, normalized to the caption of the share_type_id value. In the case of 'Other', it is defined by the event source.",
    )
    share_type_id: ShareTypeId | None = Field(
        default=None, description="The normalized identifier of the share type."
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
            ("share_type_id", "share_type", cls.ShareTypeId),
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
            data["type_uid"] = 6 * 100 + activity_id

        elif activity_id is not None and type_uid is not None:
            # Validate type_uid matches activity_id
            expected_type_uid = 6 * 100 + activity_id
            if type_uid != expected_type_uid:
                raise ValueError(
                    f"type_uid={type_uid} does not match calculated value "
                    f"(class_uid * 100 + activity_id = 6 * 100 + {activity_id} = {expected_type_uid})"
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
