from enum import Enum, property as enum_property
from typing import Any, ClassVar

from pydantic import BaseModel, model_validator

from ocsf.objects.job import Job
from ocsf.objects.kernel_driver import KernelDriver
from ocsf.objects.process import Process


class RunModeIds(Enum):
    UNKNOWN = 0
    INTERACTIVE = 1
    OWN_PROCESS = 2
    SHARED_PROCESS = 3
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return RunModeIds[obj]
        else:
            return RunModeIds(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "INTERACTIVE": "Interactive",
            "OWN_PROCESS": "Own Process",
            "SHARED_PROCESS": "Shared Process",
            "OTHER": "Other",
        }
        return name_map[super().name]


class RunStateId(Enum):
    UNKNOWN = 0
    STOPPED = 1
    START_PENDING = 2
    STOP_PENDING = 3
    RUNNING = 4
    CONTINUE_PENDING = 5
    PAUSE_PENDING = 6
    PAUSED = 7
    RESTART_PENDING = 8
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
            "STOPPED": "Stopped",
            "START_PENDING": "Start Pending",
            "STOP_PENDING": "Stop Pending",
            "RUNNING": "Running",
            "CONTINUE_PENDING": "Continue Pending",
            "PAUSE_PENDING": "Pause Pending",
            "PAUSED": "Paused",
            "RESTART_PENDING": "Restart Pending",
            "OTHER": "Other",
        }
        return name_map[super().name]


class StartTypeId(Enum):
    UNKNOWN = 0
    AUTO = 1
    BOOT = 2
    ON_DEMAND = 3
    DISABLED = 4
    ALL_LOGINS = 5
    SPECIFIC_USER_LOGIN = 6
    SCHEDULED = 7
    SYSTEM_CHANGED = 8
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return StartTypeId[obj]
        else:
            return StartTypeId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "AUTO": "Auto",
            "BOOT": "Boot",
            "ON_DEMAND": "On Demand",
            "DISABLED": "Disabled",
            "ALL_LOGINS": "All Logins",
            "SPECIFIC_USER_LOGIN": "Specific User Login",
            "SCHEDULED": "Scheduled",
            "SYSTEM_CHANGED": "System Changed",
            "OTHER": "Other",
        }
        return name_map[super().name]


class TypeId(Enum):
    UNKNOWN = 0
    KERNEL_MODE_DRIVER = 1
    USER_MODE_DRIVER = 2
    SERVICE = 3
    USER_MODE_APPLICATION = 4
    AUTOLOAD = 5
    SYSTEM_EXTENSION = 6
    KERNEL_EXTENSION = 7
    SCHEDULED_JOB__TASK = 8
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
            "KERNEL_MODE_DRIVER": "Kernel Mode Driver",
            "USER_MODE_DRIVER": "User Mode Driver",
            "SERVICE": "Service",
            "USER_MODE_APPLICATION": "User Mode Application",
            "AUTOLOAD": "Autoload",
            "SYSTEM_EXTENSION": "System Extension",
            "KERNEL_EXTENSION": "Kernel Extension",
            "SCHEDULED_JOB__TASK": "Scheduled Job, Task",
            "OTHER": "Other",
        }
        return name_map[super().name]


class StartupItem(BaseModel):
    schema_name: ClassVar[str] = "startup_item"

    # Required
    name: str
    start_type_id: StartTypeId

    # Recommended
    run_state_id: RunStateId | None = None
    type_id: TypeId | None = None

    # Optional
    driver: KernelDriver | None = None
    job: Job | None = None
    process: Process | None = None
    run_mode_ids: list[RunModeIds] | None = None
    run_modes: list[str] | None = None
    run_state: str | None = None
    start_type: str | None = None
    type_: str | None = None

    @model_validator(mode="after")
    def validate_just_one(self):
        count = len([f for f in ["driver", "job", "process"] if getattr(self, f) is not None])
        if count != 1:
            raise ValueError("Just one of `driver`, `job`, `process` must be provided, got {count}")
        return self
