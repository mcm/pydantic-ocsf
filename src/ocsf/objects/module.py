from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects.file import File
from ocsf.objects.object import Object


class LoadTypeId(Enum):
    UNKNOWN = 0
    STANDARD = 1
    NON_STANDARD = 2
    SHELLCODE = 3
    MAPPED = 4
    NONSTANDARD_BACKED = 5
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return LoadTypeId[obj]
        else:
            return LoadTypeId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "STANDARD": "Standard",
            "NON_STANDARD": "Non Standard",
            "SHELLCODE": "ShellCode",
            "MAPPED": "Mapped",
            "NONSTANDARD_BACKED": "NonStandard Backed",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Module(Object):
    schema_name: ClassVar[str] = "module"

    # Required
    load_type_id: LoadTypeId

    # Recommended
    base_address: str | None = None
    file: File | None = None
    start_address: str | None = None
    type_: str | None = None

    # Optional
    function_name: str | None = None
    load_type: str | None = None
