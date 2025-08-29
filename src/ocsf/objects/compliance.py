from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects.assessment import Assessment
from ocsf.objects.check import Check
from ocsf.objects.kb_article import KbArticle
from ocsf.objects.key_value_object import KeyValueObject
from ocsf.objects.object import Object


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


class Compliance(Object):
    schema_name: ClassVar[str] = "compliance"

    # Recommended
    control: str | None = None
    standards: list[str] | None = None
    status: str | None = None
    status_id: StatusId | None = None

    # Optional
    assessments: list[Assessment] | None = None
    category: str | None = None
    checks: list[Check] | None = None
    compliance_references: list[KbArticle] | None = None
    compliance_standards: list[KbArticle] | None = None
    control_parameters: list[KeyValueObject] | None = None
    desc: str | None = None
    requirements: list[str] | None = None
    status_code: str | None = None
    status_detail: str | None = None
    status_details: list[str] | None = None
