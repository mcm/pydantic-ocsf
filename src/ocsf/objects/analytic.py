from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects._entity import Entity


class StateId(Enum):
    UNKNOWN = 0
    ACTIVE = 1
    SUPPRESSED = 2
    EXPERIMENTAL = 3
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
            "ACTIVE": "Active",
            "SUPPRESSED": "Suppressed",
            "EXPERIMENTAL": "Experimental",
            "OTHER": "Other",
        }
        return name_map[super().name]


class TypeId(Enum):
    UNKNOWN = 0
    RULE = 1
    BEHAVIORAL = 2
    STATISTICAL = 3
    LEARNING__ML_DL_ = 4
    FINGERPRINTING = 5
    TAGGING = 6
    KEYWORD_MATCH = 7
    REGULAR_EXPRESSIONS = 8
    EXACT_DATA_MATCH = 9
    PARTIAL_DATA_MATCH = 10
    INDEXED_DATA_MATCH = 11
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
            "RULE": "Rule",
            "BEHAVIORAL": "Behavioral",
            "STATISTICAL": "Statistical",
            "LEARNING__ML_DL_": "Learning (ML/DL)",
            "FINGERPRINTING": "Fingerprinting",
            "TAGGING": "Tagging",
            "KEYWORD_MATCH": "Keyword Match",
            "REGULAR_EXPRESSIONS": "Regular Expressions",
            "EXACT_DATA_MATCH": "Exact Data Match",
            "PARTIAL_DATA_MATCH": "Partial Data Match",
            "INDEXED_DATA_MATCH": "Indexed Data Match",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Analytic(Entity):
    schema_name: ClassVar[str] = "analytic"

    # Required
    type_id: TypeId

    # Recommended
    name: str | None = None
    uid: str | None = None

    # Optional
    algorithm: str | None = None
    category: str | None = None
    desc: str | None = None
    related_analytics: list["Analytic"] | None = None
    state: str | None = None
    state_id: StateId | None = None
    type_: str | None = None
    version: str | None = None
