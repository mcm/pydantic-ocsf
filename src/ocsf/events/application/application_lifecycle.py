from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.events.application.application import Application
from ocsf.objects.product import Product


class ActivityId(Enum):
    UNKNOWN = 0
    INSTALL = 1
    REMOVE = 2
    START = 3
    STOP = 4
    RESTART = 5
    ENABLE = 6
    DISABLE = 7
    UPDATE = 8
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
            "INSTALL": "Install",
            "REMOVE": "Remove",
            "START": "Start",
            "STOP": "Stop",
            "RESTART": "Restart",
            "ENABLE": "Enable",
            "DISABLE": "Disable",
            "UPDATE": "Update",
            "OTHER": "Other",
        }
        return name_map[super().name]


class ApplicationLifecycle(Application):
    schema_name: ClassVar[str] = "application_lifecycle"
    class_id: int = 6002
    class_name: str = "Application Lifecycle"

    # Required
    activity_id: ActivityId
    app: Product
