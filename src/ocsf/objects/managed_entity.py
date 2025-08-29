from enum import Enum, property as enum_property
from typing import Any, ClassVar

from pydantic import model_validator

from ocsf.objects._entity import Entity
from ocsf.objects.device import Device
from ocsf.objects.email import Email
from ocsf.objects.group import Group
from ocsf.objects.location import Location
from ocsf.objects.organization import Organization
from ocsf.objects.policy import Policy
from ocsf.objects.user import User


class TypeId(Enum):
    UNKNOWN = 0
    DEVICE = 1
    USER = 2
    GROUP = 3
    ORGANIZATION = 4
    POLICY = 5
    EMAIL = 6
    NETWORK_ZONE = 7
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return TypeId[obj]
        else:
            return TypeId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "DEVICE": "Device",
            "USER": "User",
            "GROUP": "Group",
            "ORGANIZATION": "Organization",
            "POLICY": "Policy",
            "EMAIL": "Email",
            "NETWORK_ZONE": "Network Zone",
            "OTHER": "Other",
        }
        return name_map[super().name]


class ManagedEntity(Entity):
    schema_name: ClassVar[str] = "managed_entity"

    # Recommended
    device: Device | None = None
    email: Email | None = None
    group: Group | None = None
    name: str | None = None
    org: Organization | None = None
    policy: Policy | None = None
    type_: str | None = None
    type_id: TypeId | None = None
    uid: str | None = None
    user: User | None = None
    version: str | None = None

    # Optional
    data: dict[str, Any] | None = None
    location: Location | None = None

    @model_validator(mode="after")
    def validate_at_least_one(self):
        if all(getattr(self, field) is None for field in ["name", "uid", "device", "group", "org", "policy", "user"]):
            raise ValueError(
                "At least one of `name`, `uid`, `device`, `group`, `org`, `policy`, `user` must be provided"
            )
        return self
