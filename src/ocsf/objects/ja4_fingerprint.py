from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects.object import Object


class TypeId(Enum):
    UNKNOWN = 0
    JA4 = 1
    JA4SERVER = 2
    JA4HTTP = 3
    JA4LATENCY = 4
    JA4X509 = 5
    JA4SSH = 6
    JA4TCP = 7
    JA4TCPSERVER = 8
    JA4TCPSCAN = 9
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
            "JA4": "JA4",
            "JA4SERVER": "JA4Server",
            "JA4HTTP": "JA4HTTP",
            "JA4LATENCY": "JA4Latency",
            "JA4X509": "JA4X509",
            "JA4SSH": "JA4SSH",
            "JA4TCP": "JA4TCP",
            "JA4TCPSERVER": "JA4TCPServer",
            "JA4TCPSCAN": "JA4TCPScan",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Ja4Fingerprint(Object):
    schema_name: ClassVar[str] = "ja4_fingerprint"

    # Required
    type_id: TypeId
    value: str

    # Optional
    section_a: str | None = None
    section_b: str | None = None
    section_c: str | None = None
    section_d: str | None = None
    type_: str | None = None
