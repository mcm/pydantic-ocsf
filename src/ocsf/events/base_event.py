from datetime import datetime
from enum import Enum, property as enum_property
from typing import Any, ClassVar

from pydantic import BaseModel

from ocsf.objects.enrichment import Enrichment
from ocsf.objects.fingerprint import Fingerprint
from ocsf.objects.metadata import Metadata
from ocsf.objects.observable import Observable


class ActivityId(Enum):
    UNKNOWN = 0
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return ActivityId[obj]
        else:
            return ActivityId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "OTHER": "Other",
        }
        return name_map[super().name]


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
    SUCCESS = 1
    FAILURE = 2
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
            "SUCCESS": "Success",
            "FAILURE": "Failure",
            "OTHER": "Other",
        }
        return name_map[super().name]


class BaseEvent(BaseModel):
    schema_name: ClassVar[str] = "base_event"

    # Required
    activity_id: ActivityId
    category_uid: int = 0
    class_uid: int = 0
    metadata: Metadata
    severity_id: SeverityId
    time: datetime
    type_uid: int

    # Recommended
    message: str | None = None
    observables: list[Observable] | None = None
    status: str | None = None
    status_code: str | None = None
    status_detail: str | None = None
    status_id: StatusId | None = None
    timezone_offset: int | None = None

    # Optional
    activity_name: str | None = None
    category_name: str | None = None
    class_name: str | None = None
    count: int | None = None
    duration: int | None = None
    end_time: datetime | None = None
    enrichments: list[Enrichment] | None = None
    raw_data: str | None = None
    raw_data_hash: Fingerprint | None = None
    raw_data_size: int | None = None
    severity: str | None = None
    start_time: datetime | None = None
    type_name: str | None = None
    unmapped: dict[str, Any] | None = None

    def profile[T: BaseModel](self, profile: type[T]) -> T:
        if not profile.__pydantic_complete__:
            profile.model_rebuild(_parent_namespace_depth=3)
        return profile.model_validate(self.__pydantic_extra__)
