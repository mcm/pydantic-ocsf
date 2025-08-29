from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.events.findings.finding import Finding
from ocsf.objects.actor import Actor
from ocsf.objects.data_security import DataSecurity
from ocsf.objects.database import Database
from ocsf.objects.databucket import Databucket
from ocsf.objects.device import Device
from ocsf.objects.file import File
from ocsf.objects.network_endpoint import NetworkEndpoint
from ocsf.objects.resource_details import ResourceDetails
from ocsf.objects.table import Table


class ActivityId(Enum):
    UNKNOWN = 0
    CREATE = 1
    UPDATE = 2
    CLOSE = 3
    SUPPRESSED = 4
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
            "SUPPRESSED": "Suppressed",
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


class RiskLevelId(Enum):
    INFO = 0
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
            return RiskLevelId[obj]
        else:
            return RiskLevelId(obj)

    @enum_property
    def name(self):
        name_map = {
            "INFO": "Info",
            "LOW": "Low",
            "MEDIUM": "Medium",
            "HIGH": "High",
            "CRITICAL": "Critical",
            "OTHER": "Other",
        }
        return name_map[super().name]


class DataSecurityFinding(Finding):
    schema_name: ClassVar[str] = "data_security_finding"
    class_id: int = 2006
    class_name: str = "Data Security Finding"

    # Required
    activity_id: ActivityId

    # Recommended
    actor: Actor | None = None
    confidence_id: ConfidenceId | None = None
    data_security: DataSecurity | None = None
    database: Database | None = None
    databucket: Databucket | None = None
    device: Device | None = None
    dst_endpoint: NetworkEndpoint | None = None
    file: File | None = None
    is_alert: bool | None = None
    resources: list[ResourceDetails] | None = None
    src_endpoint: NetworkEndpoint | None = None
    table: Table | None = None

    # Optional
    activity_name: str | None = None
    confidence: str | None = None
    confidence_score: int | None = None
    impact: str | None = None
    impact_id: ImpactId | None = None
    impact_score: int | None = None
    risk_details: str | None = None
    risk_level: str | None = None
    risk_level_id: RiskLevelId | None = None
    risk_score: int | None = None
