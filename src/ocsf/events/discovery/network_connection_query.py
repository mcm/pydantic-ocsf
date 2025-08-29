from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.events.discovery.discovery_result import DiscoveryResult
from ocsf.objects.network_connection_info import NetworkConnectionInfo
from ocsf.objects.process import Process


class StateId(Enum):
    UNKNOWN = 0
    ESTABLISHED = 1
    SYN_SENT = 2
    SYN_RECV = 3
    FIN_WAIT1 = 4
    FIN_WAIT2 = 5
    TIME_WAIT = 6
    CLOSED = 7
    CLOSE_WAIT = 8
    LAST_ACK = 9
    LISTEN = 10
    CLOSING = 11
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return StateId[obj]
        else:
            return StateId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "ESTABLISHED": "ESTABLISHED",
            "SYN_SENT": "SYN_SENT",
            "SYN_RECV": "SYN_RECV",
            "FIN_WAIT1": "FIN_WAIT1",
            "FIN_WAIT2": "FIN_WAIT2",
            "TIME_WAIT": "TIME_WAIT",
            "CLOSED": "CLOSED",
            "CLOSE_WAIT": "CLOSE_WAIT",
            "LAST_ACK": "LAST_ACK",
            "LISTEN": "LISTEN",
            "CLOSING": "CLOSING",
            "OTHER": "Other",
        }
        return name_map[super().name]


class NetworkConnectionQuery(DiscoveryResult):
    schema_name: ClassVar[str] = "network_connection_query"
    class_id: int = 5012
    class_name: str = "Network Connection Query"

    # Required
    connection_info: NetworkConnectionInfo
    process: Process
    state_id: StateId

    # Recommended
    state: str | None = None
