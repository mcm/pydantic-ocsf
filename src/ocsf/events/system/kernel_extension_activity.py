from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.events.system.system import System
from ocsf.objects.actor import Actor
from ocsf.objects.kernel_driver import KernelDriver


class ActivityId(Enum):
    UNKNOWN = 0
    LOAD = 1
    UNLOAD = 2
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
            "LOAD": "Load",
            "UNLOAD": "Unload",
            "OTHER": "Other",
        }
        return name_map[super().name]


class KernelExtensionActivity(System):
    schema_name: ClassVar[str] = "kernel_extension_activity"
    class_id: int = 1002
    class_name: str = "Kernel Extension Activity"

    # Required
    activity_id: ActivityId
    actor: Actor
    driver: KernelDriver
