"""The activity ID of the event. enumeration."""

from enum import IntEnum


class FileActivityActivityId(IntEnum):
    """The activity ID of the event.

    See: https://schema.ocsf.io/1.0.0/data_types/file_activity_activity_id
    """

    UNKNOWN = 0  # The event activity is unknown.
    OTHER = 99  # The event activity is not mapped.
