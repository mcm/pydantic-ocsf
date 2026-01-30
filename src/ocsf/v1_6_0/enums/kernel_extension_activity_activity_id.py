"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class KernelExtensionActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.6.0/data_types/kernel_extension_activity_activity_id
    """

    LOAD = 1  # A driver/extension was loaded into the kernel
    UNLOAD = 2  # A driver/extension was unloaded (removed) from the kernel
