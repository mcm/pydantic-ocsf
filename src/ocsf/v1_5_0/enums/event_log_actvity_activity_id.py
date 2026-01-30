"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class EventLogActvityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.5.0/data_types/event_log_actvity_activity_id
    """

    CLEAR = 1  # Clear the event log database, file, or cache.
    DELETE = 2  # Delete the event log database, file, or cache.
    EXPORT = 3  # Export the event log database, file, or cache.
    ARCHIVE = 4  # Archive the event log database, file, or cache.
    ROTATE = 5  # Rotate the event log database, file, or cache.
    START = 6  # Start the event logging service.
    STOP = 7  # Stop the event logging service.
    RESTART = 8  # Restart the event logging service.
    ENABLE = 9  # Enable the event logging service.
    DISABLE = 10  # Disable the event logging service.
