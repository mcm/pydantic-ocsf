"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class BaseEventActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.5.0/data_types/base_event_activity_id
    """

    UNKNOWN = 0  #
    OTHER = 99  #
