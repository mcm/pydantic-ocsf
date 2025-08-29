from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects.file import File
from ocsf.objects.fingerprint import Fingerprint
from ocsf.objects.long_string import LongString
from ocsf.objects.object import Object


class TypeId(Enum):
    UNKNOWN = 0
    WINDOWS_COMMAND_PROMPT = 1
    POWERSHELL = 2
    PYTHON = 3
    JAVASCRIPT = 4
    VBSCRIPT = 5
    UNIX_SHELL = 6
    VBA = 7
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
            "WINDOWS_COMMAND_PROMPT": "Windows Command Prompt",
            "POWERSHELL": "PowerShell",
            "PYTHON": "Python",
            "JAVASCRIPT": "JavaScript",
            "VBSCRIPT": "VBScript",
            "UNIX_SHELL": "Unix Shell",
            "VBA": "VBA",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Script(Object):
    schema_name: ClassVar[str] = "script"

    # Required
    script_content: LongString
    type_id: TypeId

    # Recommended
    hashes: list[Fingerprint] | None = None

    # Optional
    file: File | None = None
    name: str | None = None
    parent_uid: str | None = None
    type_: str | None = None
    uid: str | None = None
