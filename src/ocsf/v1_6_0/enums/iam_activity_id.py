"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class IamActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.6.0/data_types/iam_activity_id
    """

    UNKNOWN = 0  #
    OTHER = 99  #
