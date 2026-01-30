"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class SystemActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.7.0/data_types/system_activity_id
    """

    UNKNOWN = 0  #
    OTHER = 99  #
