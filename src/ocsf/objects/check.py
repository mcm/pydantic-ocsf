from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects.object import Object


class SeverityId(Enum):
    UNKNOWN = 0
    INFORMATIONAL = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    CRITICAL = 5
    FATAL = 6
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return SeverityId[obj]
        else:
            return SeverityId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "INFORMATIONAL": "Informational",
            "LOW": "Low",
            "MEDIUM": "Medium",
            "HIGH": "High",
            "CRITICAL": "Critical",
            "FATAL": "Fatal",
            "OTHER": "Other",
        }
        return name_map[super().name]


class StatusId(Enum):
    UNKNOWN = 0
    PASS = 1
    WARNING = 2
    FAIL = 3
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
            "PASS": "Pass",
            "WARNING": "Warning",
            "FAIL": "Fail",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Check(Object):
    schema_name: ClassVar[str] = "check"

    # Recommended
    name: str | None = None
    standards: list[str] | None = None
    status: str | None = None
    status_id: StatusId | None = None
    uid: str | None = None

    # Optional
    desc: str | None = None
    severity: str | None = None
    severity_id: SeverityId | None = None
    version: str | None = None
