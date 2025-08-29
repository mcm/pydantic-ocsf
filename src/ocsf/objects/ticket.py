from enum import Enum, property as enum_property
from typing import Any, ClassVar

from pydantic import AnyUrl, model_validator

from ocsf.objects.object import Object


class StatusId(Enum):
    UNKNOWN = 0
    NEW = 1
    IN_PROGRESS = 2
    NOTIFIED = 3
    ON_HOLD = 4
    RESOLVED = 5
    CLOSED = 6
    CANCELED = 7
    REOPENED = 8
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return StatusId[obj]
        else:
            return StatusId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "NEW": "New",
            "IN_PROGRESS": "In Progress",
            "NOTIFIED": "Notified",
            "ON_HOLD": "On Hold",
            "RESOLVED": "Resolved",
            "CLOSED": "Closed",
            "CANCELED": "Canceled",
            "REOPENED": "Reopened",
            "OTHER": "Other",
        }
        return name_map[super().name]


class TypeId(Enum):
    UNKNOWN = 0
    INTERNAL = 1
    EXTERNAL = 2
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
            "INTERNAL": "Internal",
            "EXTERNAL": "External",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Ticket(Object):
    schema_name: ClassVar[str] = "ticket"

    # Recommended
    src_url: AnyUrl | None = None
    uid: str | None = None

    # Optional
    status: str | None = None
    status_details: list[str] | None = None
    status_id: StatusId | None = None
    title: str | None = None
    type_: str | None = None
    type_id: TypeId | None = None

    @model_validator(mode="after")
    def validate_at_least_one(self):
        if all(getattr(self, field) is None for field in ["src_url", "uid"]):
            raise ValueError("At least one of `src_url`, `uid` must be provided")
        return self
