"""Query Evidence object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_6_0.enums.query_evidence_tcp_state_id import QueryEvidenceTcpStateId
    from ocsf.v1_6_0.objects.file import File
    from ocsf.v1_6_0.objects.group import Group
    from ocsf.v1_6_0.objects.job import Job
    from ocsf.v1_6_0.objects.kernel import Kernel
    from ocsf.v1_6_0.objects.module import Module
    from ocsf.v1_6_0.objects.network_connection_info import NetworkConnectionInfo
    from ocsf.v1_6_0.objects.network_interface import NetworkInterface
    from ocsf.v1_6_0.objects.peripheral_device import PeripheralDevice
    from ocsf.v1_6_0.objects.process import Process
    from ocsf.v1_6_0.objects.service import Service
    from ocsf.v1_6_0.objects.session import Session
    from ocsf.v1_6_0.objects.startup_item import StartupItem
    from ocsf.v1_6_0.objects.user import User


class QueryEvidence(OCSFBaseModel):
    """The specific resulting evidence information that was queried or discovered. When mapping raw telemetry data users should select the appropriate child object that best matches the evidence type as defined by query_type_id.

    See: https://schema.ocsf.io/1.6.0/objects/query_evidence
    """

    # Nested Enums for sibling attribute pairs
    class QueryTypeId(SiblingEnum):
        """The normalized type of system query performed against a device or system component.

        OCSF Attribute: query_type_id
        """

        UNKNOWN = 0
        KERNEL = 1
        FILE = 2
        FOLDER = 3
        ADMIN_GROUP = 4
        JOB = 5
        MODULE = 6
        NETWORK_CONNECTION = 7
        NETWORK_INTERFACES = 8
        PERIPHERAL_DEVICE = 9
        PROCESS = 10
        SERVICE = 11
        SESSION = 12
        USER = 13
        USERS = 14
        STARTUP_ITEM = 15
        REGISTRY_KEY = 16
        REGISTRY_VALUE = 17
        PREFETCH = 18
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Kernel",
                2: "File",
                3: "Folder",
                4: "Admin Group",
                5: "Job",
                6: "Module",
                7: "Network Connection",
                8: "Network Interfaces",
                9: "Peripheral Device",
                10: "Process",
                11: "Service",
                12: "Session",
                13: "User",
                14: "Users",
                15: "Startup Item",
                16: "Registry Key",
                17: "Registry Value",
                18: "Prefetch",
                99: "Other",
            }

    query_type_id: QueryTypeId = Field(
        ...,
        description="The normalized type of system query performed against a device or system component.",
    )
    connection_info: NetworkConnectionInfo | None = Field(
        default=None,
        description="The network connection information related to a Network Connection query type. [Recommended]",
    )
    file: File | None = Field(
        default=None,
        description="The file that is the target of the query when query_type_id indicates a File query. [Recommended]",
    )
    folder: File | None = Field(
        default=None,
        description="The folder that is the target of the query when query_type_id indicates a Folder query. [Recommended]",
    )
    group: Group | None = Field(
        default=None,
        description="The administrative group that is the target of the query when query_type_id indicates an Admin Group query. [Recommended]",
    )
    job: Job | None = Field(
        default=None,
        description="The job object that pertains to the event when query_type_id indicates a Job query. [Recommended]",
    )
    kernel: Kernel | None = Field(
        default=None,
        description="The kernel object that pertains to the event when query_type_id indicates a Kernel query. [Recommended]",
    )
    module: Module | None = Field(
        default=None,
        description="The module that pertains to the event when query_type_id indicates a Module query. [Recommended]",
    )
    network_interfaces: list[NetworkInterface] | None = Field(
        default=None,
        description="The physical or virtual network interfaces that are associated with the device when query_type_id indicates a Network Interfaces query. [Recommended]",
    )
    peripheral_device: PeripheralDevice | None = Field(
        default=None,
        description="The peripheral device that triggered the event when query_type_id indicates a Peripheral Device query. [Recommended]",
    )
    process: Process | None = Field(
        default=None,
        description="The process that pertains to the event when query_type_id indicates a Process query. [Recommended]",
    )
    query_type: str | None = Field(
        default=None,
        description="The normalized caption of query_type_id or the source-specific query type.",
    )
    service: Service | None = Field(
        default=None,
        description="The service that pertains to the event when query_type_id indicates a Service query. [Recommended]",
    )
    session: Session | None = Field(
        default=None,
        description="The authenticated user or service session when query_type_id indicates a Session query. [Recommended]",
    )
    startup_item: StartupItem | None = Field(
        default=None,
        description="The startup item object that pertains to the event when query_type_id indicates a Startup Item query. [Recommended]",
    )
    state: str | None = Field(
        default=None,
        description="The state of the socket, normalized to the caption of the state_id value. In the case of 'Other', it is defined by the event source.",
    )
    tcp_state_id: QueryEvidenceTcpStateId | None = Field(
        default=None, description="The state of the TCP socket for the network connection."
    )
    user: User | None = Field(
        default=None,
        description="The user that pertains to the event when query_type_id indicates a User query. [Recommended]",
    )
    users: list[User] | None = Field(
        default=None,
        description="The users that belong to the administrative group when query_type_id indicates a Users query.",
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
            ("query_type_id", "query_type", cls.QueryTypeId),
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
