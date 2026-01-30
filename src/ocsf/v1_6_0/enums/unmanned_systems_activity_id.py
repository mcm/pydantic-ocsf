"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class UnmannedSystemsActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.6.0/data_types/unmanned_systems_activity_id
    """

    UNKNOWN = 0  #
    OTHER = 99  #
