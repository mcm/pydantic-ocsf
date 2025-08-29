from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.events.findings.finding import Finding
from ocsf.objects.anomaly_analysis import AnomalyAnalysis
from ocsf.objects.evidences import Evidences
from ocsf.objects.malware import Malware
from ocsf.objects.malware_scan_info import MalwareScanInfo
from ocsf.objects.remediation import Remediation
from ocsf.objects.resource_details import ResourceDetails
from ocsf.objects.vulnerability import Vulnerability


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


class DetectionFinding(Finding):
    schema_name: ClassVar[str] = "detection_finding"
    class_id: int = 2004
    class_name: str = "Detection Finding"

    # Recommended
    confidence_id: ConfidenceId | None = None
    evidences: list[Evidences] | None = None
    is_alert: bool | None = None
    resources: list[ResourceDetails] | None = None

    # Optional
    anomaly_analyses: list[AnomalyAnalysis] | None = None
    confidence: str | None = None
    confidence_score: int | None = None
    impact: str | None = None
    impact_id: ImpactId | None = None
    impact_score: int | None = None
    malware: list[Malware] | None = None
    malware_scan_info: MalwareScanInfo | None = None
    remediation: Remediation | None = None
    risk_details: str | None = None
    risk_level: str | None = None
    risk_level_id: RiskLevelId | None = None
    risk_score: int | None = None
    vulnerabilities: list[Vulnerability] | None = None
