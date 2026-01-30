"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class ModuleActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.7.0/data_types/module_activity_activity_id
    """

    LOAD = 1  # The target module was loaded.
    UNLOAD = 2  # The target module was unloaded.
    INVOKE = 3  # A function exported from the target module was invoked.
