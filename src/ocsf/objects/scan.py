from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects._entity import Entity


class TypeId(Enum):
    UNKNOWN = 0
    MANUAL = 1
    SCHEDULED = 2
    UPDATED_CONTENT = 3
    QUARANTINED_ITEMS = 4
    ATTACHED_MEDIA = 5
    USER_LOGON = 6
    ELAM = 7
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
            "MANUAL": "Manual",
            "SCHEDULED": "Scheduled",
            "UPDATED_CONTENT": "Updated Content",
            "QUARANTINED_ITEMS": "Quarantined Items",
            "ATTACHED_MEDIA": "Attached Media",
            "USER_LOGON": "User Logon",
            "ELAM": "ELAM",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Scan(Entity):
    schema_name: ClassVar[str] = "scan"

    # Required
    type_id: TypeId

    # Recommended
    name: str | None = None
    uid: str | None = None

    # Optional
    type_: str | None = None
