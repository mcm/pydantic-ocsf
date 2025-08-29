from enum import Enum, property as enum_property
from typing import Any, ClassVar

from pydantic import model_validator

from ocsf.events.system.system import System
from ocsf.objects.actor import Actor
from ocsf.objects.device import Device
from ocsf.objects.file import File
from ocsf.objects.network_endpoint import NetworkEndpoint


class ActivityId(Enum):
    UNKNOWN = 0
    CLEAR = 1
    DELETE = 2
    EXPORT = 3
    ARCHIVE = 4
    ROTATE = 5
    START = 6
    STOP = 7
    RESTART = 8
    ENABLE = 9
    DISABLE = 10
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
            "CLEAR": "Clear",
            "DELETE": "Delete",
            "EXPORT": "Export",
            "ARCHIVE": "Archive",
            "ROTATE": "Rotate",
            "START": "Start",
            "STOP": "Stop",
            "RESTART": "Restart",
            "ENABLE": "Enable",
            "DISABLE": "Disable",
            "OTHER": "Other",
        }
        return name_map[super().name]


class LogTypeId(Enum):
    UNKNOWN = 0
    OS = 1
    APPLICATION = 2
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return LogTypeId[obj]
        else:
            return LogTypeId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "OS": "OS",
            "APPLICATION": "Application",
            "OTHER": "Other",
        }
        return name_map[super().name]


class EventLogActivity(System):
    schema_name: ClassVar[str] = "event_log_activity"
    class_id: int = 1008
    class_name: str = "Event Log Activity"

    # Required
    activity_id: ActivityId

    # Recommended
    actor: Actor | None = None
    device: Device | None = None
    dst_endpoint: NetworkEndpoint | None = None
    file: File | None = None
    log_name: str | None = None
    log_provider: str | None = None
    log_type: str | None = None
    log_type_id: LogTypeId | None = None
    src_endpoint: NetworkEndpoint | None = None
    status_code: str | None = None
    status_detail: str | None = None

    @model_validator(mode="after")
    def validate_at_least_one(self):
        if all(
            getattr(self, field) is None
            for field in ["log_file", "log_name", "log_provider", "log_type", "log_type_id"]
        ):
            raise ValueError(
                "At least one of `log_file`, `log_name`, `log_provider`, `log_type`, `log_type_id` must be provided"
            )
        return self
