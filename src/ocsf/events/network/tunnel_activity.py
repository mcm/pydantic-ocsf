from enum import Enum, property as enum_property
from typing import Any, ClassVar

from pydantic import model_validator

from ocsf.events.network.network import Network
from ocsf.objects.device import Device
from ocsf.objects.network_connection_info import NetworkConnectionInfo
from ocsf.objects.network_endpoint import NetworkEndpoint
from ocsf.objects.network_interface import NetworkInterface
from ocsf.objects.network_traffic import NetworkTraffic
from ocsf.objects.session import Session
from ocsf.objects.user import User


class ActivityId(Enum):
    UNKNOWN = 0
    OPEN = 1
    CLOSE = 2
    RENEW = 3
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return ActivityId[obj]
        else:
            return ActivityId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "OPEN": "Open",
            "CLOSE": "Close",
            "RENEW": "Renew",
            "OTHER": "Other",
        }
        return name_map[super().name]


class TunnelTypeId(Enum):
    UNKNOWN = 0
    SPLIT_TUNNEL = 1
    FULL_TUNNEL = 2
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return TunnelTypeId[obj]
        else:
            return TunnelTypeId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "SPLIT_TUNNEL": "Split Tunnel",
            "FULL_TUNNEL": "Full Tunnel",
            "OTHER": "Other",
        }
        return name_map[super().name]


class TunnelActivity(Network):
    schema_name: ClassVar[str] = "tunnel_activity"
    class_id: int = 4014
    class_name: str = "Tunnel Activity"

    # Required
    activity_id: ActivityId

    # Recommended
    device: Device | None = None
    dst_endpoint: NetworkEndpoint | None = None
    session: Session | None = None
    src_endpoint: NetworkEndpoint | None = None
    tunnel_interface: NetworkInterface | None = None
    tunnel_type: str | None = None
    tunnel_type_id: TunnelTypeId | None = None
    user: User | None = None

    # Optional
    connection_info: NetworkConnectionInfo | None = None
    protocol_name: str | None = None
    traffic: NetworkTraffic | None = None

    @model_validator(mode="after")
    def validate_at_least_one(self):
        if all(
            getattr(self, field) is None
            for field in ["connection_info", "session", "src_endpoint", "traffic", "tunnel_interface", "tunnel_type_id"]
        ):
            raise ValueError(
                "At least one of `connection_info`, `session`, `src_endpoint`, `traffic`, `tunnel_interface`, `tunnel_type_id` must be provided"
            )
        return self
