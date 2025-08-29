from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects.object import Object


class TypeId(Enum):
    UNKNOWN = 0
    SHARED_MUTEX = 1
    SYSTEM_CALL = 2
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
            "SHARED_MUTEX": "Shared Mutex",
            "SYSTEM_CALL": "System Call",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Kernel(Object):
    schema_name: ClassVar[str] = "kernel"

    # Required
    name: str
    type_id: TypeId

    # Optional
    is_system: bool | None = None
    path: str | None = None
    system_call: str | None = None
    type_: str | None = None
