from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects.object import Object


class TypeId(Enum):
    UNKNOWN = 0
    NATION_STATE = 1
    CYBERCRIMINAL = 2
    HACKTIVISTS = 3
    INSIDER = 4
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
            "NATION_STATE": "Nation-state",
            "CYBERCRIMINAL": "Cybercriminal",
            "HACKTIVISTS": "Hacktivists",
            "INSIDER": "Insider",
            "OTHER": "Other",
        }
        return name_map[super().name]


class ThreatActor(Object):
    schema_name: ClassVar[str] = "threat_actor"

    # Required
    name: str

    # Recommended
    type_id: TypeId | None = None

    # Optional
    type_: str | None = None
