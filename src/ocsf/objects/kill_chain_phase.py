from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects.object import Object


class PhaseId(Enum):
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
    schema_name: ClassVar[str] = "kill_chain_phase"

    # Required
    phase_id: PhaseId

    # Recommended
    phase: str | None = None
