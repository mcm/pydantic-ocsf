from enum import Enum, property as enum_property
from typing import Any, ClassVar

from pydantic import model_validator

from ocsf.objects.data_classification import DataClassification
from ocsf.objects.policy import Policy


class DataLifecycleStateId(Enum):
    UNKNOWN = 0
    DATA_AT_REST = 1
    DATA_IN_TRANSIT = 2
    DATA_IN_USE = 3
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return DataLifecycleStateId[obj]
        else:
            return DataLifecycleStateId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "DATA_AT_REST": "Data at-Rest",
            "DATA_IN_TRANSIT": "Data in-Transit",
            "DATA_IN_USE": "Data in-Use",
            "OTHER": "Other",
        }
        return name_map[super().name]


class DetectionSystemId(Enum):
    UNKNOWN = 0
    ENDPOINT = 1
    DLP_GATEWAY = 2
    MOBILE_DEVICE_MANAGEMENT = 3
    DATA_DISCOVERY___CLASSIFICATION = 4
    SECURE_WEB_GATEWAY = 5
    SECURE_EMAIL_GATEWAY = 6
    DIGITAL_RIGHTS_MANAGEMENT = 7
    CLOUD_ACCESS_SECURITY_BROKER = 8
    DATABASE_ACTIVITY_MONITORING = 9
    APPLICATION_LEVEL_DLP = 10
    DEVELOPER_SECURITY = 11
    DATA_SECURITY_POSTURE_MANAGEMENT = 12
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return DetectionSystemId[obj]
        else:
            return DetectionSystemId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "ENDPOINT": "Endpoint",
            "DLP_GATEWAY": "DLP Gateway",
            "MOBILE_DEVICE_MANAGEMENT": "Mobile Device Management",
            "DATA_DISCOVERY___CLASSIFICATION": "Data Discovery & Classification",
            "SECURE_WEB_GATEWAY": "Secure Web Gateway",
            "SECURE_EMAIL_GATEWAY": "Secure Email Gateway",
            "DIGITAL_RIGHTS_MANAGEMENT": "Digital Rights Management",
            "CLOUD_ACCESS_SECURITY_BROKER": "Cloud Access Security Broker",
            "DATABASE_ACTIVITY_MONITORING": "Database Activity Monitoring",
            "APPLICATION_LEVEL_DLP": "Application-Level DLP",
            "DEVELOPER_SECURITY": "Developer Security",
            "DATA_SECURITY_POSTURE_MANAGEMENT": "Data Security Posture Management",
            "OTHER": "Other",
        }
        return name_map[super().name]


class DataSecurity(DataClassification):
    schema_name: ClassVar[str] = "data_security"

    # Recommended
    data_lifecycle_state_id: DataLifecycleStateId | None = None
    detection_pattern: str | None = None
    detection_system_id: DetectionSystemId | None = None
    policy: Policy | None = None

    # Optional
    data_lifecycle_state: str | None = None
    detection_system: str | None = None
    pattern_match: str | None = None

    @model_validator(mode="after")
    def validate_at_least_one(self):
        if all(
            getattr(self, field) is None
            for field in ["data_lifecycle_state_id", "detection_pattern", "detection_system_id", "policy"]
        ):
            raise ValueError(
                "At least one of `data_lifecycle_state_id`, `detection_pattern`, `detection_system_id`, `policy` must be provided"
            )
        return self
