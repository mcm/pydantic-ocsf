from enum import Enum, property as enum_property
from typing import Any, ClassVar
from uuid import UUID

from ocsf.objects.display import Display
from ocsf.objects.keyboard_info import KeyboardInfo
from ocsf.objects.object import Object


class CpuArchitectureId(Enum):
    UNKNOWN = 0
    X86 = 1
    ARM = 2
    RISC_V = 3
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return CpuArchitectureId[obj]
        else:
            return CpuArchitectureId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "X86": "x86",
            "ARM": "ARM",
            "RISC_V": "RISC-V",
            "OTHER": "Other",
        }
        return name_map[super().name]


class DeviceHwInfo(Object):
    schema_name: ClassVar[str] = "device_hw_info"

    # Optional
    bios_date: str | None = None
    bios_manufacturer: str | None = None
    bios_ver: str | None = None
    chassis: str | None = None
    cpu_architecture: str | None = None
    cpu_architecture_id: CpuArchitectureId | None = None
    cpu_bits: int | None = None
    cpu_cores: int | None = None
    cpu_count: int | None = None
    cpu_speed: int | None = None
    cpu_type: str | None = None
    desktop_display: Display | None = None
    keyboard_info: KeyboardInfo | None = None
    ram_size: int | None = None
    serial_number: str | None = None
    uuid: UUID | None = None
    vendor_name: str | None = None
