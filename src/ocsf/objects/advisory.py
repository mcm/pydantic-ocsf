from datetime import datetime
from enum import Enum, property as enum_property
from typing import Any, ClassVar

from pydantic import AnyUrl

from ocsf.objects.cve import Cve
from ocsf.objects.cwe import Cwe
from ocsf.objects.object import Object
from ocsf.objects.os import Os
from ocsf.objects.product import Product
from ocsf.objects.timespan import Timespan


class InstallStateId(Enum):
    UNKNOWN = 0
    INSTALLED = 1
    NOT_INSTALLED = 2
    INSTALLED_PENDING_REBOOT = 3
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return InstallStateId[obj]
        else:
            return InstallStateId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "INSTALLED": "Installed",
            "NOT_INSTALLED": "Not Installed",
            "INSTALLED_PENDING_REBOOT": "Installed Pending Reboot",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Advisory(Object):
    schema_name: ClassVar[str] = "advisory"

    # Required
    uid: str

    # Recommended
    created_time: datetime | None = None
    install_state: str | None = None
    install_state_id: InstallStateId | None = None
    os: Os | None = None
    references: list[str] | None = None
    title: str | None = None

    # Optional
    avg_timespan: Timespan | None = None
    bulletin: str | None = None
    classification: str | None = None
    desc: str | None = None
    is_superseded: bool | None = None
    modified_time: datetime | None = None
    product: Product | None = None
    related_cves: list[Cve] | None = None
    related_cwes: list[Cwe] | None = None
    size: int | None = None
    src_url: AnyUrl | None = None
