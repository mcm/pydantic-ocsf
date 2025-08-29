import re
from enum import IntEnum, property as enum_property
from typing import Any, ClassVar, Self

from pydantic import ModelWrapValidatorHandler, computed_field, model_validator

from ocsf.objects.object import Object
from ocsf.objects.reputation import Reputation


class TypeId(IntEnum):
    UNKNOWN = 0
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return TypeId[obj]
        else:
            return TypeId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Observable(Object):
    allowed_profiles: ClassVar[None] = None
    schema_name: ClassVar[str] = "observable"

    # Required
    type_id: TypeId

    # Recommended
    name: str | None = None

    # Optional
    reputation: Reputation | None = None
    value: str | None = None

    @computed_field  # type: ignore[misc,prop-decorator]
    @property
    def type(self) -> str:
        return self.type_id.name

    @type.setter
    def type(self, value: str) -> None:
        self.type_id = TypeId[value]

    @model_validator(mode="wrap")
    @classmethod
    def validate_type(cls, data: dict[str, Any], handler: ModelWrapValidatorHandler) -> Self:
        if "type" in data and "type_id" not in data:
            type = re.sub(r"\W", "_", data.pop("type").upper())
            data["type_id"] = TypeId[type]
        instance = handler(data)
        if instance.__pydantic_extra__ and "type" in instance.__pydantic_extra__:
            instance.__pydantic_extra__.pop("type")
        return instance
