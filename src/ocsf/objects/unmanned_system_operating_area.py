from datetime import datetime
from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects.location import Location


class TypeId(Enum):
    UNKNOWN_UNDECLARED = 0
    TAKEOFF_LOCATION = 1
    FIXED_LOCATION = 2
    DYNAMIC_LOCATION = 3
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
            "UNKNOWN_UNDECLARED": "Unknown/Undeclared",
            "TAKEOFF_LOCATION": "Takeoff Location",
            "FIXED_LOCATION": "Fixed Location",
            "DYNAMIC_LOCATION": "Dynamic Location",
            "OTHER": "Other",
        }
        return name_map[super().name]


class UnmannedSystemOperatingArea(Location):
    schema_name: ClassVar[str] = "unmanned_system_operating_area"

    # Recommended
    count: int | None = None
    locations: list[Location] | None = None
    type_id: TypeId | None = None

    # Optional
    altitude_ceiling: str | None = None
    altitude_floor: str | None = None
    end_time: datetime | None = None
    radius: str | None = None
    start_time: datetime | None = None
    type_: str | None = None
