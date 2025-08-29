from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.events.network.network import Network


class ActivityId(Enum):
    UNKNOWN = 0
    SYMMETRIC_ACTIVE_EXCHANGE = 1
    SYMMETRIC_PASSIVE_RESPONSE = 2
    CLIENT_SYNCHRONIZATION = 3
    SERVER_RESPONSE = 4
    BROADCAST = 5
    CONTROL = 6
    PRIVATE_USE_CASE = 7
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
            "SYMMETRIC_ACTIVE_EXCHANGE": "Symmetric Active Exchange",
            "SYMMETRIC_PASSIVE_RESPONSE": "Symmetric Passive Response",
            "CLIENT_SYNCHRONIZATION": "Client Synchronization",
            "SERVER_RESPONSE": "Server Response",
            "BROADCAST": "Broadcast",
            "CONTROL": "Control",
            "PRIVATE_USE_CASE": "Private Use Case",
            "OTHER": "Other",
        }
        return name_map[super().name]


class StratumId(Enum):
    UNKNOWN = 0
    PRIMARY_SERVER = 1
    SECONDARY_SERVER = 2
    UNSYNCHRONIZED = 16
    RESERVED = 17
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return StratumId[obj]
        else:
            return StratumId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "PRIMARY_SERVER": "Primary Server",
            "SECONDARY_SERVER": "Secondary Server",
            "UNSYNCHRONIZED": "Unsynchronized",
            "RESERVED": "Reserved",
            "OTHER": "Other",
        }
        return name_map[super().name]


class NtpActivity(Network):
    schema_name: ClassVar[str] = "ntp_activity"
    class_id: int = 4013
    class_name: str = "NTP Activity"

    # Required
    activity_id: ActivityId
    version: str

    # Recommended
    delay: int | None = None
    dispersion: int | None = None
    precision: int | None = None
    stratum: str | None = None
    stratum_id: StratumId | None = None
