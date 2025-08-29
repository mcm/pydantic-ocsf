from enum import Enum, property as enum_property
from typing import Any, ClassVar
from uuid import UUID

from ocsf.objects.aircraft import Aircraft
from ocsf.objects.device_hw_info import DeviceHwInfo
from ocsf.objects.location import Location


class TypeId(Enum):
    UNKNOWN_UNDECLARED = 0
    AIRPLANE = 1
    HELICOPTER = 2
    GYROPLANE = 3
    HYBRID_LIFT = 4
    ORNITHOPTER = 5
    GLIDER = 6
    KITE = 7
    FREE_BALLOON = 8
    CAPTIVE_BALLOON = 9
    AIRSHIP = 10
    FREE_FALL_PARACHUTE = 11
    ROCKET = 12
    TETHERED_POWERED_AIRCRAFT = 13
    GROUND_OBSTACLE = 14
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
            "AIRPLANE": "Airplane",
            "HELICOPTER": "Helicopter",
            "GYROPLANE": "Gyroplane",
            "HYBRID_LIFT": "Hybrid Lift",
            "ORNITHOPTER": "Ornithopter",
            "GLIDER": "Glider",
            "KITE": "Kite",
            "FREE_BALLOON": "Free Balloon",
            "CAPTIVE_BALLOON": "Captive Balloon",
            "AIRSHIP": "Airship",
            "FREE_FALL_PARACHUTE": "Free Fall/Parachute",
            "ROCKET": "Rocket",
            "TETHERED_POWERED_AIRCRAFT": "Tethered Powered Aircraft",
            "GROUND_OBSTACLE": "Ground Obstacle",
            "OTHER": "Other",
        }
        return name_map[super().name]


class UnmannedAerialSystem(Aircraft):
    schema_name: ClassVar[str] = "unmanned_aerial_system"

    # Recommended
    location: Location | None = None
    serial_number: str | None = None
    type_id: TypeId | None = None
    uid: str | None = None
    uid_alt: str | None = None
    uuid: UUID | None = None

    # Optional
    hw_info: DeviceHwInfo | None = None
    name: str | None = None
    type_: str | None = None
