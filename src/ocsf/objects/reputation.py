from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects.object import Object


class ScoreId(Enum):
    UNKNOWN = 0
    VERY_SAFE = 1
    SAFE = 2
    PROBABLY_SAFE = 3
    LEANS_SAFE = 4
    MAY_NOT_BE_SAFE = 5
    EXERCISE_CAUTION = 6
    SUSPICIOUS_RISKY = 7
    POSSIBLY_MALICIOUS = 8
    PROBABLY_MALICIOUS = 9
    MALICIOUS = 10
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return ScoreId[obj]
        else:
            return ScoreId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "VERY_SAFE": "Very Safe",
            "SAFE": "Safe",
            "PROBABLY_SAFE": "Probably Safe",
            "LEANS_SAFE": "Leans Safe",
            "MAY_NOT_BE_SAFE": "May not be Safe",
            "EXERCISE_CAUTION": "Exercise Caution",
            "SUSPICIOUS_RISKY": "Suspicious/Risky",
            "POSSIBLY_MALICIOUS": "Possibly Malicious",
            "PROBABLY_MALICIOUS": "Probably Malicious",
            "MALICIOUS": "Malicious",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Reputation(Object):
    schema_name: ClassVar[str] = "reputation"

    # Required
    base_score: float
    score_id: ScoreId

    # Recommended
    provider: str | None = None

    # Optional
    score: str | None = None
