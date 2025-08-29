from datetime import datetime
from enum import Enum, property as enum_property
from typing import Any, ClassVar

from pydantic import AnyUrl, model_validator

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


class KbArticle(Object):
    schema_name: ClassVar[str] = "kb_article"

    # Recommended
    install_state: str | None = None
    install_state_id: InstallStateId | None = None
    os: Os | None = None
    severity: str | None = None
    title: str | None = None
    uid: str | None = None

    # Optional
    avg_timespan: Timespan | None = None
    bulletin: str | None = None
    classification: str | None = None
    created_time: datetime | None = None
    is_superseded: bool | None = None
    product: Product | None = None
    size: int | None = None
    src_url: AnyUrl | None = None

    @model_validator(mode="after")
    def validate_at_least_one(self):
        if all(getattr(self, field) is None for field in ["uid", "src_url"]):
            raise ValueError("At least one of `uid`, `src_url` must be provided")
        return self
