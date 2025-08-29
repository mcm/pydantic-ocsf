from datetime import datetime
from enum import Enum, property as enum_property
from typing import Annotated, Any, ClassVar, Literal

from pydantic import Field

from ocsf.events.base_event import BaseEvent
from ocsf.objects.device import Device
from ocsf.objects.finding_info import FindingInfo
from ocsf.objects.vendor_attributes import VendorAttributes


class ActivityId(Enum):
    UNKNOWN = 0
    CREATE = 1
    UPDATE = 2
    CLOSE = 3
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
            "CREATE": "Create",
            "UPDATE": "Update",
            "CLOSE": "Close",
            "OTHER": "Other",
        }
        return name_map[super().name]


class ConfidenceId(Enum):
    UNKNOWN = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return ConfidenceId[obj]
        else:
            return ConfidenceId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "LOW": "Low",
            "MEDIUM": "Medium",
            "HIGH": "High",
            "OTHER": "Other",
        }
        return name_map[super().name]


class StatusId(Enum):
    UNKNOWN = 0
    NEW = 1
    IN_PROGRESS = 2
    SUPPRESSED = 3
    RESOLVED = 4
    ARCHIVED = 5
    DELETED = 6
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
            "NEW": "New",
            "IN_PROGRESS": "In Progress",
            "SUPPRESSED": "Suppressed",
            "RESOLVED": "Resolved",
            "ARCHIVED": "Archived",
            "DELETED": "Deleted",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Finding(BaseEvent):
    schema_name: ClassVar[str] = "finding"
    category_name: Annotated[Literal["Findings"], Field(frozen=True)] = "Findings"
    category_uid: Annotated[Literal[2], Field(frozen=True)] = 2

    # Required
    activity_id: ActivityId
    finding_info: FindingInfo

    # Recommended
    confidence_id: ConfidenceId | None = None
    status_id: StatusId | None = None

    # Optional
    activity_name: str | None = None
    comment: str | None = None
    confidence: str | None = None
    confidence_score: int | None = None
    device: Device | None = None
    end_time: datetime | None = None
    start_time: datetime | None = None
    status: str | None = None
    vendor_attributes: VendorAttributes | None = None
