"""The normalized identifier of the finding activity. enumeration."""

from enum import IntEnum


class FindingActivityId(IntEnum):
    """The normalized identifier of the finding activity.

    See: https://schema.ocsf.io/1.2.0/data_types/finding_activity_id
    """

    CREATE = 1  # A finding was created.
    UPDATE = 2  # A finding was updated.
    CLOSE = 3  # A finding was closed.
