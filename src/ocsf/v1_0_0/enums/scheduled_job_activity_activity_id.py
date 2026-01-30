"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class ScheduledJobActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.0.0/data_types/scheduled_job_activity_activity_id
    """

    CREATE = 1  #
    UPDATE = 2  #
    DELETE = 3  #
    ENABLE = 4  #
    DISABLE = 5  #
    START = 6  #
