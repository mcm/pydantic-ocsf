"""The normalized identifier of the CPU architecture. enumeration."""

from enum import IntEnum


class DeviceHwInfoCpuArchitectureId(IntEnum):
    """The normalized identifier of the CPU architecture.

    See: https://schema.ocsf.io/1.5.0/data_types/device_hw_info_cpu_architecture_id
    """

    UNKNOWN = 0  # The CPU architecture is unknown.
    X86 = 1  # CPU uses the x86 ISA. For bitness, refer to <code>cpu_bits</code>.
    ARM = 2  # CPU uses the ARM ISA. For bitness, refer to <code>cpu_bits</code>.
    RISC_V = 3  # CPU uses the RISC-V ISA. For bitness, refer to <code>cpu_bits</code>.
    OTHER = 99  # The CPU architecture is not mapped. See the <code>cpu_architecture</code> attribute, which contains a data source specific value.
