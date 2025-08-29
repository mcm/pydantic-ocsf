from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.events.iam.iam import IAM
from ocsf.objects.managed_entity import ManagedEntity


class ActivityId(Enum):
    UNKNOWN = 0
    CREATE = 1
    READ = 2
    UPDATE = 3
    DELETE = 4
    MOVE = 5
    ENROLL = 6
    UNENROLL = 7
    ENABLE = 8
    DISABLE = 9
    ACTIVATE = 10
    DEACTIVATE = 11
    SUSPEND = 12
    RESUME = 13
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
            "CREATE": "Create",
            "READ": "Read",
            "UPDATE": "Update",
            "DELETE": "Delete",
            "MOVE": "Move",
            "ENROLL": "Enroll",
            "UNENROLL": "Unenroll",
            "ENABLE": "Enable",
            "DISABLE": "Disable",
            "ACTIVATE": "Activate",
            "DEACTIVATE": "Deactivate",
            "SUSPEND": "Suspend",
            "RESUME": "Resume",
            "OTHER": "Other",
        }
        return name_map[super().name]


class EntityManagement(IAM):
    schema_name: ClassVar[str] = "entity_management"
    class_id: int = 3004
    class_name: str = "Entity Management"

    # Required
    activity_id: ActivityId
    entity: ManagedEntity

    # Recommended
    comment: str | None = None
    entity_result: ManagedEntity | None = None

    # Optional
    access_list: list[str] | None = None
    access_mask: int | None = None
