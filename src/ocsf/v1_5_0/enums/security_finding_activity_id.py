"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class SecurityFindingActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.5.0/data_types/security_finding_activity_id
    """

    CREATE = 1  # A security finding was created.
    UPDATE = 2  # A security finding was updated.
    CLOSE = 3  # A security finding was closed.
