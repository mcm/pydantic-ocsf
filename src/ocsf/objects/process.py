from datetime import datetime
from enum import Enum, property as enum_property
from typing import Any, ClassVar

from pydantic import model_validator

from ocsf.objects.environment_variable import EnvironmentVariable
from ocsf.objects.file import File
from ocsf.objects.process_entity import ProcessEntity
from ocsf.objects.session import Session
from ocsf.objects.user import User


class IntegrityId(Enum):
    UNKNOWN = 0
    UNTRUSTED = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    SYSTEM = 5
    PROTECTED = 6
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return IntegrityId[obj]
        else:
            return IntegrityId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "UNTRUSTED": "Untrusted",
            "LOW": "Low",
            "MEDIUM": "Medium",
            "HIGH": "High",
            "SYSTEM": "System",
            "PROTECTED": "Protected",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Process(ProcessEntity):
    schema_name: ClassVar[str] = "process"

    # Recommended
    file: File | None = None
    parent_process: "Process | None" = None
    user: User | None = None

    # Optional
    ancestry: list[ProcessEntity] | None = None
    environment_variables: list[EnvironmentVariable] | None = None
    integrity: str | None = None
    integrity_id: IntegrityId | None = None
    lineage: list[str] | None = None
    loaded_modules: list[str] | None = None
    ptid: int | None = None
    sandbox: str | None = None
    session: Session | None = None
    terminated_time: datetime | None = None
    tid: int | None = None
    working_directory: str | None = None
    xattributes: dict[str, Any] | None = None

    @model_validator(mode="after")
    def validate_at_least_one(self):
        if all(getattr(self, field) is None for field in ["pid", "uid", "cpid"]):
            raise ValueError("At least one of `pid`, `uid`, `cpid` must be provided")
        return self
