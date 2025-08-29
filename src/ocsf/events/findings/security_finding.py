from enum import Enum, property as enum_property
from typing import Annotated, Any, ClassVar, Literal

from pydantic import Field

from ocsf.events.base_event import BaseEvent
from ocsf.objects.analytic import Analytic
from ocsf.objects.attack import Attack
from ocsf.objects.cis_csc import CisCsc
from ocsf.objects.compliance import Compliance
from ocsf.objects.finding import Finding
from ocsf.objects.kill_chain_phase import KillChainPhase
from ocsf.objects.malware import Malware
from ocsf.objects.process import Process
from ocsf.objects.resource_details import ResourceDetails
from ocsf.objects.vulnerability import Vulnerability


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


class StateId(Enum):
    UNKNOWN = 0
    NEW = 1
    IN_PROGRESS = 2
    SUPPRESSED = 3
    RESOLVED = 4
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return StateId[obj]
        else:
            return StateId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "NEW": "New",
            "IN_PROGRESS": "In Progress",
            "SUPPRESSED": "Suppressed",
            "RESOLVED": "Resolved",
            "OTHER": "Other",
        }
        return name_map[super().name]


class SecurityFinding(BaseEvent):
    schema_name: ClassVar[str] = "security_finding"
    category_name: Annotated[Literal["Findings"], Field(frozen=True)] = "Findings"
    category_uid: Annotated[Literal[2], Field(frozen=True)] = 2

    # Required
    activity_id: ActivityId
    finding: Finding
    state_id: StateId

    # Recommended
    analytic: Analytic | None = None
    confidence: str | None = None
    confidence_id: ConfidenceId | None = None
    confidence_score: int | None = None
    impact: str | None = None
    impact_id: ImpactId | None = None
    impact_score: int | None = None
    resources: list[ResourceDetails] | None = None
    risk_level: str | None = None
    risk_level_id: RiskLevelId | None = None
    risk_score: int | None = None

    # Optional
    attacks: list[Attack] | None = None
    cis_csc: list[CisCsc] | None = None
    compliance: Compliance | None = None
    data_sources: list[str] | None = None
    evidence: dict[str, Any] | None = None
    kill_chain: list[KillChainPhase] | None = None
    malware: list[Malware] | None = None
    nist: list[str] | None = None
    process: Process | None = None
    state: str | None = None
    vulnerabilities: list[Vulnerability] | None = None
