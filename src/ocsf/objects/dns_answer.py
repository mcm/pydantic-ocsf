from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects._dns import Dns


class FlagIds(Enum):
    UNKNOWN = 0
    AUTHORITATIVE_ANSWER = 1
    TRUNCATED_RESPONSE = 2
    RECURSION_DESIRED = 3
    RECURSION_AVAILABLE = 4
    AUTHENTIC_DATA = 5
    CHECKING_DISABLED = 6
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return FlagIds[obj]
        else:
            return FlagIds(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "AUTHORITATIVE_ANSWER": "Authoritative Answer",
            "TRUNCATED_RESPONSE": "Truncated Response",
            "RECURSION_DESIRED": "Recursion Desired",
            "RECURSION_AVAILABLE": "Recursion Available",
            "AUTHENTIC_DATA": "Authentic Data",
            "CHECKING_DISABLED": "Checking Disabled",
            "OTHER": "Other",
        }
        return name_map[super().name]


class DnsAnswer(Dns):
    schema_name: ClassVar[str] = "dns_answer"

    # Required
    rdata: str

    # Recommended
    class_: str | None = None
    flag_ids: list[FlagIds] | None = None
    ttl: int | None = None
    type_: str | None = None

    # Optional
    flags: list[str] | None = None
