from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects.fingerprint import Fingerprint
from ocsf.objects.object import Object


class RelationshipId(Enum):
    UNKNOWN = 0
    DEPENDS_ON = 1
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return RelationshipId[obj]
        else:
            return RelationshipId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "DEPENDS_ON": "Depends On",
            "OTHER": "Other",
        }
        return name_map[super().name]


class TypeId(Enum):
    UNKNOWN = 0
    FRAMEWORK = 1
    LIBRARY = 2
    OPERATING_SYSTEM = 3
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
            "FRAMEWORK": "Framework",
            "LIBRARY": "Library",
            "OPERATING_SYSTEM": "Operating System",
            "OTHER": "Other",
        }
        return name_map[super().name]


class SoftwareComponent(Object):
    schema_name: ClassVar[str] = "software_component"

    # Required
    name: str
    version: str

    # Recommended
    author: str | None = None
    purl: str | None = None
    related_component: str | None = None
    relationship_id: RelationshipId | None = None
    type_id: TypeId | None = None

    # Optional
    hash: Fingerprint | None = None
    license: str | None = None
    relationship: str | None = None
    type_: str | None = None
