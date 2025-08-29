from datetime import datetime
from enum import Enum, property as enum_property
from typing import Annotated, Any, ClassVar, Literal

from pydantic import AnyUrl, Field, model_validator

from ocsf.events.base_event import BaseEvent
from ocsf.objects.attack import Attack
from ocsf.objects.finding_info import FindingInfo
from ocsf.objects.group import Group
from ocsf.objects.ticket import Ticket
from ocsf.objects.user import User
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


class ImpactId(Enum):
    UNKNOWN = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return ImpactId[obj]
        else:
            return ImpactId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "LOW": "Low",
            "MEDIUM": "Medium",
            "HIGH": "High",
            "CRITICAL": "Critical",
            "OTHER": "Other",
        }
        return name_map[super().name]


class PriorityId(Enum):
    UNKNOWN = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return PriorityId[obj]
        else:
            return PriorityId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "LOW": "Low",
            "MEDIUM": "Medium",
            "HIGH": "High",
            "CRITICAL": "Critical",
            "OTHER": "Other",
        }
        return name_map[super().name]


class StatusId(Enum):
    UNKNOWN = 0
    NEW = 1
    IN_PROGRESS = 2
    ON_HOLD = 3
    RESOLVED = 4
    CLOSED = 5
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
            "ON_HOLD": "On Hold",
            "RESOLVED": "Resolved",
            "CLOSED": "Closed",
            "OTHER": "Other",
        }
        return name_map[super().name]


class VerdictId(Enum):
    UNKNOWN = 0
    FALSE_POSITIVE = 1
    TRUE_POSITIVE = 2
    DISREGARD = 3
    SUSPICIOUS = 4
    BENIGN = 5
    TEST = 6
    INSUFFICIENT_DATA = 7
    SECURITY_RISK = 8
    MANAGED_EXTERNALLY = 9
    DUPLICATE = 10
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return VerdictId[obj]
        else:
            return VerdictId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "FALSE_POSITIVE": "False Positive",
            "TRUE_POSITIVE": "True Positive",
            "DISREGARD": "Disregard",
            "SUSPICIOUS": "Suspicious",
            "BENIGN": "Benign",
            "TEST": "Test",
            "INSUFFICIENT_DATA": "Insufficient Data",
            "SECURITY_RISK": "Security Risk",
            "MANAGED_EXTERNALLY": "Managed Externally",
            "DUPLICATE": "Duplicate",
            "OTHER": "Other",
        }
        return name_map[super().name]


class IncidentFinding(BaseEvent):
    schema_name: ClassVar[str] = "incident_finding"
    category_name: Annotated[Literal["Findings"], Field(frozen=True)] = "Findings"
    category_uid: Annotated[Literal[2], Field(frozen=True)] = 2

    # Required
    activity_id: ActivityId
    finding_info_list: list[FindingInfo]
    status_id: StatusId

    # Recommended
    confidence_id: ConfidenceId | None = None
    desc: str | None = None
    impact: str | None = None
    impact_id: ImpactId | None = None
    impact_score: int | None = None
    priority_id: PriorityId | None = None
    src_url: AnyUrl | None = None
    status: str | None = None
    verdict: str | None = None
    verdict_id: VerdictId | None = None

    # Optional
    activity_name: str | None = None
    assignee: User | None = None
    assignee_group: Group | None = None
    attacks: list[Attack] | None = None
    comment: str | None = None
    confidence: str | None = None
    confidence_score: int | None = None
    end_time: datetime | None = None
    is_suspected_breach: bool | None = None
    priority: str | None = None
    start_time: datetime | None = None
    ticket: Ticket | None = None
    tickets: list[Ticket] | None = None
    vendor_attributes: VendorAttributes | None = None

    @model_validator(mode="after")
    def validate_at_least_one(self):
        if all(getattr(self, field) is None for field in ["assignee", "assignee_group"]):
            raise ValueError("At least one of `assignee`, `assignee_group` must be provided")
        return self
