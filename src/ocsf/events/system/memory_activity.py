from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.events.system.system import System
from ocsf.objects.process import Process


class ActivityId(Enum):
    UNKNOWN = 0
    ALLOCATE_PAGE = 1
    MODIFY_PAGE = 2
    DELETE_PAGE = 3
    BUFFER_OVERFLOW = 4
    DISABLE_DEP = 5
    ENABLE_DEP = 6
    READ = 7
    WRITE = 8
    MAP_VIEW = 9
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
            "ALLOCATE_PAGE": "Allocate Page",
            "MODIFY_PAGE": "Modify Page",
            "DELETE_PAGE": "Delete Page",
            "BUFFER_OVERFLOW": "Buffer Overflow",
            "DISABLE_DEP": "Disable DEP",
            "ENABLE_DEP": "Enable DEP",
            "READ": "Read",
            "WRITE": "Write",
            "MAP_VIEW": "Map View",
            "OTHER": "Other",
        }
        return name_map[super().name]


class MemoryActivity(System):
    schema_name: ClassVar[str] = "memory_activity"
    class_id: int = 1004
    class_name: str = "Memory Activity"

    # Required
    activity_id: ActivityId
    process: Process

    # Recommended
    actual_permissions: int | None = None
    base_address: str | None = None
    requested_permissions: int | None = None
    size: int | None = None
