from enum import Enum, property as enum_property
from typing import Any, ClassVar

from pydantic import AnyUrl

from ocsf.objects.fingerprint import Fingerprint
from ocsf.objects.object import Object


class TypeId(Enum):
    UNKNOWN = 0
    APPLICATION = 1
    OPERATING_SYSTEM = 2
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
            "APPLICATION": "Application",
            "OPERATING_SYSTEM": "Operating System",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Package(Object):
    schema_name: ClassVar[str] = "package"

    # Required
    name: str
    version: str

    # Recommended
    architecture: str | None = None
    type_id: TypeId | None = None

    # Optional
    cpe_name: str | None = None
    epoch: int | None = None
    hash: Fingerprint | None = None
    license: str | None = None
    license_url: AnyUrl | None = None
    package_manager: str | None = None
    package_manager_url: AnyUrl | None = None
    purl: str | None = None
    release: str | None = None
    src_url: AnyUrl | None = None
    type_: str | None = None
    uid: str | None = None
    vendor_name: str | None = None
