from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.events.system.system import System
from ocsf.objects.script import Script


class ActivityId(Enum):
    UNKNOWN = 0
    EXECUTE = 1
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
            "EXECUTE": "Execute",
            "OTHER": "Other",
        }
        return name_map[super().name]


class ScriptActivity(System):
    schema_name: ClassVar[str] = "script_activity"
    class_id: int = 1009
    class_name: str = "Script Activity"

    # Required
    activity_id: ActivityId
    script: Script
