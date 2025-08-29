from datetime import datetime
from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects.file import File
from ocsf.objects.object import Object
from ocsf.objects.user import User


class RunStateId(Enum):
    UNKNOWN = 0
    READY = 1
    QUEUED = 2
    RUNNING = 3
    STOPPED = 4
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return RunStateId[obj]
        else:
            return RunStateId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "READY": "Ready",
            "QUEUED": "Queued",
            "RUNNING": "Running",
            "STOPPED": "Stopped",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Job(Object):
    schema_name: ClassVar[str] = "job"

    # Required
    file: File
    name: str

    # Recommended
    cmd_line: str | None = None
    created_time: datetime | None = None
    desc: str | None = None
    last_run_time: datetime | None = None
    run_state_id: RunStateId | None = None

    # Optional
    next_run_time: datetime | None = None
    run_state: str | None = None
    user: User | None = None
