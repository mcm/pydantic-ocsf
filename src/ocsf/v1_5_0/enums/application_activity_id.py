"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class ApplicationActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.5.0/data_types/application_activity_id
    """

    UNKNOWN = 0  #
    OTHER = 99  #
