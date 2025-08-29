from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects.object import Object
from ocsf.objects.session import Session


class BoundaryId(Enum):
    UNKNOWN = 0
    LOCALHOST = 1
    INTERNAL = 2
    EXTERNAL = 3
    SAME_VPC = 4
    INTERNET_VPC_GATEWAY = 5
    VIRTUAL_PRIVATE_GATEWAY = 6
    INTRA_REGION_VPC = 7
    INTER_REGION_VPC = 8
    LOCAL_GATEWAY = 9
    GATEWAY_VPC = 10
    INTERNET_GATEWAY = 11
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return BoundaryId[obj]
        else:
            return BoundaryId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "LOCALHOST": "Localhost",
            "INTERNAL": "Internal",
            "EXTERNAL": "External",
            "SAME_VPC": "Same VPC",
            "INTERNET_VPC_GATEWAY": "Internet/VPC Gateway",
            "VIRTUAL_PRIVATE_GATEWAY": "Virtual Private Gateway",
            "INTRA_REGION_VPC": "Intra-region VPC",
            "INTER_REGION_VPC": "Inter-region VPC",
            "LOCAL_GATEWAY": "Local Gateway",
            "GATEWAY_VPC": "Gateway VPC",
            "INTERNET_GATEWAY": "Internet Gateway",
            "OTHER": "Other",
        }
        return name_map[super().name]


class DirectionId(Enum):
    UNKNOWN = 0
    INBOUND = 1
    OUTBOUND = 2
    LATERAL = 3
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return DirectionId[obj]
        else:
            return DirectionId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "INBOUND": "Inbound",
            "OUTBOUND": "Outbound",
            "LATERAL": "Lateral",
            "OTHER": "Other",
        }
        return name_map[super().name]


class ProtocolVerId(Enum):
    UNKNOWN = 0
    INTERNET_PROTOCOL_VERSION_4__IPV4_ = 4
    INTERNET_PROTOCOL_VERSION_6__IPV6_ = 6
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return ProtocolVerId[obj]
        else:
            return ProtocolVerId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "INTERNET_PROTOCOL_VERSION_4__IPV4_": "Internet Protocol version 4 (IPv4)",
            "INTERNET_PROTOCOL_VERSION_6__IPV6_": "Internet Protocol version 6 (IPv6)",
            "OTHER": "Other",
        }
        return name_map[super().name]


class NetworkConnectionInfo(Object):
    schema_name: ClassVar[str] = "network_connection_info"

    # Required
    direction_id: DirectionId

    # Recommended
    boundary_id: BoundaryId | None = None
    protocol_name: str | None = None
    protocol_num: int | None = None
    protocol_ver_id: ProtocolVerId | None = None
    uid: str | None = None

    # Optional
    boundary: str | None = None
    community_uid: str | None = None
    direction: str | None = None
    flag_history: str | None = None
    protocol_ver: str | None = None
    session: Session | None = None
    tcp_flags: int | None = None
