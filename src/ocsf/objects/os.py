from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects.object import Object


class TypeId(Enum):
    UNKNOWN = 0
    OTHER = 99
    WINDOWS = 100
    WINDOWS_MOBILE = 101
    LINUX = 200
    ANDROID = 201
    MACOS = 300
    IOS = 301
    IPADOS = 302
    SOLARIS = 400
    AIX = 401
    HP_UX = 402

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
            "WINDOWS": "Windows",
            "WINDOWS_MOBILE": "Windows Mobile",
            "LINUX": "Linux",
            "ANDROID": "Android",
            "MACOS": "macOS",
            "IOS": "iOS",
            "IPADOS": "iPadOS",
            "SOLARIS": "Solaris",
            "AIX": "AIX",
            "HP_UX": "HP-UX",
        }
        return name_map[super().name]


class Os(Object):
    schema_name: ClassVar[str] = "os"

    # Required
    name: str
    type_id: TypeId

    # Optional
    build: str | None = None
    country: str | None = None
    cpe_name: str | None = None
    cpu_bits: int | None = None
    edition: str | None = None
    kernel_release: str | None = None
    lang: str | None = None
    sp_name: str | None = None
    sp_ver: int | None = None
    type_: str | None = None
    version: str | None = None
