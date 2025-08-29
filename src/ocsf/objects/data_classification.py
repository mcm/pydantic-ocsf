from enum import Enum, property as enum_property
from typing import Any, ClassVar

from pydantic import AnyUrl, model_validator

from ocsf.objects.classifier_details import ClassifierDetails
from ocsf.objects.discovery_details import DiscoveryDetails
from ocsf.objects.object import Object
from ocsf.objects.policy import Policy


class CategoryId(Enum):
    UNKNOWN = 0
    PERSONAL = 1
    GOVERNMENTAL = 2
    FINANCIAL = 3
    BUSINESS = 4
    MILITARY_AND_LAW_ENFORCEMENT = 5
    SECURITY = 6
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return CategoryId[obj]
        else:
            return CategoryId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "PERSONAL": "Personal",
            "GOVERNMENTAL": "Governmental",
            "FINANCIAL": "Financial",
            "BUSINESS": "Business",
            "MILITARY_AND_LAW_ENFORCEMENT": "Military and Law Enforcement",
            "SECURITY": "Security",
            "OTHER": "Other",
        }
        return name_map[super().name]


class ConfidentialityId(Enum):
    UNKNOWN = 0
    NOT_CONFIDENTIAL = 1
    CONFIDENTIAL = 2
    SECRET = 3
    TOP_SECRET = 4
    PRIVATE = 5
    RESTRICTED = 6
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return ConfidentialityId[obj]
        else:
            return ConfidentialityId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "NOT_CONFIDENTIAL": "Not Confidential",
            "CONFIDENTIAL": "Confidential",
            "SECRET": "Secret",
            "TOP_SECRET": "Top Secret",
            "PRIVATE": "Private",
            "RESTRICTED": "Restricted",
            "OTHER": "Other",
        }
        return name_map[super().name]


class StatusId(Enum):
    UNKNOWN = 0
    COMPLETE = 1
    PARTIAL = 2
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
            "COMPLETE": "Complete",
            "PARTIAL": "Partial",
            "FAIL": "Fail",
            "OTHER": "Other",
        }
        return name_map[super().name]


class DataClassification(Object):
    schema_name: ClassVar[str] = "data_classification"

    # Recommended
    category_id: CategoryId | None = None
    classifier_details: ClassifierDetails | None = None
    confidentiality_id: ConfidentialityId | None = None
    status: str | None = None
    status_id: StatusId | None = None

    # Optional
    category: str | None = None
    confidentiality: str | None = None
    discovery_details: list[DiscoveryDetails] | None = None
    policy: Policy | None = None
    size: int | None = None
    src_url: AnyUrl | None = None
    status_details: list[str] | None = None
    total: int | None = None
    uid: str | None = None

    @model_validator(mode="after")
    def validate_at_least_one(self):
        if all(getattr(self, field) is None for field in ["category_id", "confidentiality_id"]):
            raise ValueError("At least one of `category_id`, `confidentiality_id` must be provided")
        return self
