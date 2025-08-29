from enum import Enum, property as enum_property
from typing import Any, ClassVar

from pydantic import model_validator

from ocsf.objects.object import Object
from ocsf.objects.policy import Policy


class TypeId(Enum):
    UNKNOWN = 0
    ENDPOINT_DETECTION_AND_RESPONSE = 1
    DATA_LOSS_PREVENTION = 2
    BACKUP___RECOVERY = 3
    PERFORMANCE_MONITORING___OBSERVABILITY = 4
    VULNERABILITY_MANAGEMENT = 5
    LOG_FORWARDING = 6
    MOBILE_DEVICE_MANAGEMENT = 7
    CONFIGURATION_MANAGEMENT = 8
    REMOTE_ACCESS = 9
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return TypeId[obj]
        else:
            return TypeId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "ENDPOINT_DETECTION_AND_RESPONSE": "Endpoint Detection and Response",
            "DATA_LOSS_PREVENTION": "Data Loss Prevention",
            "BACKUP___RECOVERY": "Backup & Recovery",
            "PERFORMANCE_MONITORING___OBSERVABILITY": "Performance Monitoring & Observability",
            "VULNERABILITY_MANAGEMENT": "Vulnerability Management",
            "LOG_FORWARDING": "Log Forwarding",
            "MOBILE_DEVICE_MANAGEMENT": "Mobile Device Management",
            "CONFIGURATION_MANAGEMENT": "Configuration Management",
            "REMOTE_ACCESS": "Remote Access",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Agent(Object):
    schema_name: ClassVar[str] = "agent"

    # Recommended
    name: str | None = None
    type_id: TypeId | None = None
    uid: str | None = None

    # Optional
    policies: list[Policy] | None = None
    type_: str | None = None
    uid_alt: str | None = None
    vendor_name: str | None = None
    version: str | None = None

    @model_validator(mode="after")
    def validate_at_least_one(self):
        if all(getattr(self, field) is None for field in ["uid", "name"]):
            raise ValueError("At least one of `uid`, `name` must be provided")
        return self
