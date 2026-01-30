"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class ApplicationLifecycleActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.0.0/data_types/application_lifecycle_activity_id
    """

    INSTALL = 1  #
    REMOVE = 2  #
    START = 3  #
    STOP = 4  #
