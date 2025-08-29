from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.events.discovery.discovery import Discovery
from ocsf.objects.actor import Actor
from ocsf.objects.device import Device
from ocsf.objects.security_state import SecurityState


class PrevSecurityLevelId(Enum):
    UNKNOWN = 0
    SECURE = 1
    AT_RISK = 2
    COMPROMISED = 3
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return PrevSecurityLevelId[obj]
        else:
            return PrevSecurityLevelId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "SECURE": "Secure",
            "AT_RISK": "At Risk",
            "COMPROMISED": "Compromised",
            "OTHER": "Other",
        }
        return name_map[super().name]


class SecurityLevelId(Enum):
    UNKNOWN = 0
    SECURE = 1
    AT_RISK = 2
    COMPROMISED = 3
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return SecurityLevelId[obj]
        else:
            return SecurityLevelId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "SECURE": "Secure",
            "AT_RISK": "At Risk",
            "COMPROMISED": "Compromised",
            "OTHER": "Other",
        }
        return name_map[super().name]


class StateId(Enum):
    UNKNOWN = 0
    DISABLED = 1
    ENABLED = 2
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
            "DISABLED": "Disabled",
            "ENABLED": "Enabled",
            "OTHER": "Other",
        }
        return name_map[super().name]


class DeviceConfigStateChange(Discovery):
    schema_name: ClassVar[str] = "device_config_state_change"
    class_id: int = 5019
    class_name: str = "Device Config State Change"

    # Required
    device: Device

    # Recommended
    prev_security_level: str | None = None
    prev_security_level_id: PrevSecurityLevelId | None = None
    prev_security_states: list[SecurityState] | None = None
    security_level: str | None = None
    security_level_id: SecurityLevelId | None = None
    security_states: list[SecurityState] | None = None
    state_id: StateId | None = None

    # Optional
    actor: Actor | None = None
    state: str | None = None
