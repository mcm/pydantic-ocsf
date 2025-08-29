import re
from enum import IntEnum, property as enum_property
from typing import Any, ClassVar, Self

from pydantic import ModelWrapValidatorHandler, computed_field, model_validator

from ocsf.objects.object import Object


class SeverityId(IntEnum):
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


class VendorAttributes(Object):
    allowed_profiles: ClassVar[None] = None
    schema_name: ClassVar[str] = "vendor_attributes"

    # Optional
    severity_id: SeverityId | None = None

    @computed_field  # type: ignore[misc,prop-decorator]
    @property
    def severity(self) -> str | None:
        if self.severity_id is None:
            return None
        return self.severity_id.name

    @severity.setter
    def severity(self, value: str | None) -> None:
        if value is None:
            self.severity_id = None
        else:
            self.severity_id = SeverityId[value]

    @model_validator(mode="wrap")
    @classmethod
    def validate_severity(cls, data: dict[str, Any], handler: ModelWrapValidatorHandler) -> Self:
        if "severity" in data and "severity_id" not in data:
            severity = re.sub(r"\W", "_", data.pop("severity").upper())
            data["severity_id"] = SeverityId[severity]
        instance = handler(data)
        if instance.__pydantic_extra__ and "severity" in instance.__pydantic_extra__:
            instance.__pydantic_extra__.pop("severity")
        return instance
