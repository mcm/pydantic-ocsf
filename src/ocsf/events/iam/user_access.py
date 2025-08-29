from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.events.iam.iam import IAM
from ocsf.objects.resource_details import ResourceDetails
from ocsf.objects.user import User


class ActivityId(Enum):
    UNKNOWN = 0
    ASSIGN_PRIVILEGES = 1
    REVOKE_PRIVILEGES = 2
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
            "ASSIGN_PRIVILEGES": "Assign Privileges",
            "REVOKE_PRIVILEGES": "Revoke Privileges",
            "OTHER": "Other",
        }
        return name_map[super().name]


class UserAccess(IAM):
    schema_name: ClassVar[str] = "user_access"
    class_id: int = 3005
    class_name: str = "User Access Management"

    # Required
    activity_id: ActivityId
    privileges: list[str]
    user: User

    # Recommended
    resource: ResourceDetails | None = None
    resources: list[ResourceDetails] | None = None
