"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class ModuleActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.6.0/data_types/module_activity_activity_id
    """

    LOAD = 1  #
    UNLOAD = 2  #
