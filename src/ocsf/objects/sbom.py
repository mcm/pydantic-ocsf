from datetime import datetime
from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects.object import Object
from ocsf.objects.package import Package
from ocsf.objects.product import Product
from ocsf.objects.software_component import SoftwareComponent


class TypeId(Enum):
    UNKNOWN = 0
    SPDX = 1
    CYCLONEDX = 2
    SWID = 3
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
            "SPDX": "SPDX",
            "CYCLONEDX": "CycloneDX",
            "SWID": "SWID",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Sbom(Object):
    schema_name: ClassVar[str] = "sbom"

    # Required
    package: Package
    software_components: list[SoftwareComponent]

    # Recommended
    created_time: datetime | None = None
    product: Product | None = None
    type_id: TypeId | None = None

    # Optional
    type_: str | None = None
    uid: str | None = None
    version: str | None = None
