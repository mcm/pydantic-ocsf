"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class FindingsActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.0.0/data_types/findings_activity_id
    """

    CREATE = 1  # A security finding is created.
    UPDATE = 2  # A security finding is updated.
