from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects.object import Object
from ocsf.objects.policy import Policy


class StatusId(Enum):
    UNKNOWN = 0
    APPLICABLE = 1
    INAPPLICABLE = 2
    EVALUATION_ERROR = 3
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
            "APPLICABLE": "Applicable",
            "INAPPLICABLE": "Inapplicable",
            "EVALUATION_ERROR": "Evaluation Error",
            "OTHER": "Other",
        }
        return name_map[super().name]


class AdditionalRestriction(Object):
    schema_name: ClassVar[str] = "additional_restriction"

    # Required
    policy: Policy

    # Recommended
    status_id: StatusId | None = None

    # Optional
    status: str | None = None
