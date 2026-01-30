"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class ProcessActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.6.0/data_types/process_activity_activity_id
    """

    LAUNCH = 1  #
    TERMINATE = 2  #
    OPEN = 3  #
    INJECT = 4  #
    SET_USER_ID = 5  #
