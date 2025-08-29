from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.events.network.network import Network
from ocsf.objects.network_endpoint import NetworkEndpoint
from ocsf.objects.url import Url


class ActivityId(Enum):
    UNKNOWN = 0
    OPEN = 1
    CLOSE = 2
    RESET = 3
    FAIL = 4
    REFUSE = 5
    TRAFFIC = 6
    LISTEN = 7
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
            "RESET": "Reset",
            "FAIL": "Fail",
            "REFUSE": "Refuse",
            "TRAFFIC": "Traffic",
            "LISTEN": "Listen",
            "OTHER": "Other",
        }
        return name_map[super().name]


class NetworkActivity(Network):
    schema_name: ClassVar[str] = "network_activity"
    class_id: int = 4001
    class_name: str = "Network Activity"

    # Required
    activity_id: ActivityId

    # Recommended
    dst_endpoint: NetworkEndpoint | None = None
    is_src_dst_assignment_known: bool | None = None
    src_endpoint: NetworkEndpoint | None = None
    url: Url | None = None
