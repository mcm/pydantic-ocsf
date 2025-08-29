from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.events.system.system import System
from ocsf.objects.actor import Actor
from ocsf.objects.module import Module
from ocsf.objects.process import Process


class ActivityId(Enum):
    UNKNOWN = 0
    LAUNCH = 1
    TERMINATE = 2
    OPEN = 3
    INJECT = 4
    SET_USER_ID = 5
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
            "LAUNCH": "Launch",
            "TERMINATE": "Terminate",
            "OPEN": "Open",
            "INJECT": "Inject",
            "SET_USER_ID": "Set User ID",
            "OTHER": "Other",
        }
        return name_map[super().name]


class InjectionTypeId(Enum):
    UNKNOWN = 0
    REMOTE_THREAD = 1
    LOAD_LIBRARY = 2
    QUEUE_APC = 3
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return InjectionTypeId[obj]
        else:
            return InjectionTypeId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "REMOTE_THREAD": "Remote Thread",
            "LOAD_LIBRARY": "Load Library",
            "QUEUE_APC": "Queue APC",
            "OTHER": "Other",
        }
        return name_map[super().name]


class ProcessActivity(System):
    schema_name: ClassVar[str] = "process_activity"
    class_id: int = 1007
    class_name: str = "Process Activity"

    # Required
    activity_id: ActivityId
    actor: Actor
    process: Process

    # Recommended
    actual_permissions: int | None = None
    exit_code: int | None = None
    injection_type: str | None = None
    injection_type_id: InjectionTypeId | None = None
    module: Module | None = None
    requested_permissions: int | None = None
