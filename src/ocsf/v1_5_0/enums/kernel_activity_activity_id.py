"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class KernelActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.5.0/data_types/kernel_activity_activity_id
    """

    CREATE = 1  #
    READ = 2  #
    DELETE = 3  #
    INVOKE = 4  #
