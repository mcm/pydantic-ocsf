"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class KernelActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.0.0/data_types/kernel_activity_activity_id
    """

    UNKNOWN = 0  # The event activity is unknown.
    OTHER = 99  # The event activity is not mapped.
