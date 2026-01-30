"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class ApplicationLifecycleActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.5.0/data_types/application_lifecycle_activity_id
    """

    INSTALL = 1  # Install the application.
    REMOVE = 2  # Remove the application.
    START = 3  # Start the application.
    STOP = 4  # Stop the application.
    RESTART = 5  # Restart the application.
    ENABLE = 6  # Enable the application.
    DISABLE = 7  # Disable the application.
    UPDATE = 8  # Update the application.
