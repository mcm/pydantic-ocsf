from enum import Enum, property as enum_property
from typing import Any, ClassVar

from pydantic import model_validator

from ocsf.events.iam.iam import IAM
from ocsf.objects.group import Group
from ocsf.objects.network_endpoint import NetworkEndpoint
from ocsf.objects.session import Session
from ocsf.objects.user import User


class ActivityId(Enum):
    UNKNOWN = 0
    ASSIGN_PRIVILEGES = 1
    ASSIGN_GROUPS = 2
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
            "ASSIGN_GROUPS": "Assign Groups",
            "OTHER": "Other",
        }
        return name_map[super().name]


class AuthorizeSession(IAM):
    schema_name: ClassVar[str] = "authorize_session"
    class_id: int = 3003
    class_name: str = "Authorize Session"

    # Required
    activity_id: ActivityId
    user: User

    # Recommended
    group: Group | None = None
    privileges: list[str] | None = None
    session: Session | None = None

    # Optional
    dst_endpoint: NetworkEndpoint | None = None

    @model_validator(mode="after")
    def validate_just_one(self):
        count = len([f for f in ["privileges", "group"] if getattr(self, f) is not None])
        if count != 1:
            raise ValueError("Just one of `privileges`, `group` must be provided, got {count}")
        return self
