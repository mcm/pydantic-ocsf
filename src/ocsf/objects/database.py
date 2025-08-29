from datetime import datetime
from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects._entity import Entity
from ocsf.objects.group import Group


class TypeId(Enum):
    UNKNOWN = 0
    RELATIONAL = 1
    NETWORK = 2
    OBJECT_ORIENTED = 3
    CENTRALIZED = 4
    OPERATIONAL = 5
    NOSQL = 6
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
            "RELATIONAL": "Relational",
            "NETWORK": "Network",
            "OBJECT_ORIENTED": "Object Oriented",
            "CENTRALIZED": "Centralized",
            "OPERATIONAL": "Operational",
            "NOSQL": "NoSQL",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Database(Entity):
    schema_name: ClassVar[str] = "database"

    # Required
    type_id: TypeId

    # Recommended
    name: str | None = None
    type_: str | None = None
    uid: str | None = None

    # Optional
    created_time: datetime | None = None
    desc: str | None = None
    groups: list[Group] | None = None
    modified_time: datetime | None = None
    size: int | None = None
