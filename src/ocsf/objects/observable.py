from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects.object import Object
from ocsf.objects.reputation import Reputation


class TypeId(Enum):
    UNKNOWN = 0
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
            "OTHER": "Other",
        }
        return name_map[super().name]


class Observable(Object):
    schema_name: ClassVar[str] = "observable"

    # Required
    type_id: TypeId

    # Recommended
    name: str | None = None

    # Optional
    reputation: Reputation | None = None
    type_: str | None = None
    value: str | None = None
