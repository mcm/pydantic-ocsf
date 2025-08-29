import re
from enum import IntEnum, property as enum_property
from typing import Any, ClassVar, Self

from pydantic import ModelWrapValidatorHandler, computed_field, model_validator

from ocsf.objects.object import Object


class PhaseId(IntEnum):
    UNKNOWN = 0
    RECONNAISSANCE = 1
    WEAPONIZATION = 2
    DELIVERY = 3
    EXPLOITATION = 4
    INSTALLATION = 5
    COMMAND___CONTROL = 6
    ACTIONS_ON_OBJECTIVES = 7
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return PhaseId[obj]
        else:
            return PhaseId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "RECONNAISSANCE": "Reconnaissance",
            "WEAPONIZATION": "Weaponization",
            "DELIVERY": "Delivery",
            "EXPLOITATION": "Exploitation",
            "INSTALLATION": "Installation",
            "COMMAND___CONTROL": "Command & Control",
            "ACTIONS_ON_OBJECTIVES": "Actions on Objectives",
            "OTHER": "Other",
        }
        return name_map[super().name]


class KillChainPhase(Object):
    allowed_profiles: ClassVar[None] = None
    schema_name: ClassVar[str] = "kill_chain_phase"

    # Required
    phase_id: PhaseId

    @computed_field  # type: ignore[misc,prop-decorator]
    @property
    def phase(self) -> str:
        return self.phase_id.name

    @phase.setter
    def phase(self, value: str) -> None:
        self.phase_id = PhaseId[value]

    @model_validator(mode="wrap")
    @classmethod
    def validate_phase(cls, data: dict[str, Any], handler: ModelWrapValidatorHandler) -> Self:
        if "phase" in data and "phase_id" not in data:
            phase = re.sub(r"\W", "_", data.pop("phase").upper())
            data["phase_id"] = PhaseId[phase]
        instance = handler(data)
        if instance.__pydantic_extra__ and "phase" in instance.__pydantic_extra__:
            instance.__pydantic_extra__.pop("phase")
        return instance
