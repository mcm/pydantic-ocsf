"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class DiscoveryResultActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.1.0/data_types/discovery_result_activity_id
    """

    EXISTS = 1  # The target was found.
    PARTIAL = 2  # The target was partially found.
    DOES_NOT_EXIST = 3  # The target was not found.
    ERROR = 4  # The discovery attempt failed.
    UNSUPPORTED = 5  # Discovery of the target was not supported.
