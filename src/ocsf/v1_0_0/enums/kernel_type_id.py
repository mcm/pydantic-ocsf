"""The type of the kernel resource. enumeration."""

from enum import IntEnum


class KernelTypeId(IntEnum):
    """The type of the kernel resource.

    See: https://schema.ocsf.io/1.0.0/data_types/kernel_type_id
    """

    SHARED_MUTEX = 1  #
    SYSTEM_CALL = 2  #
