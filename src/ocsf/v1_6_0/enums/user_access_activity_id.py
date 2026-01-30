"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class UserAccessActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.6.0/data_types/user_access_activity_id
    """

    ASSIGN_PRIVILEGES = 1  # Assign privileges to a user.
    REVOKE_PRIVILEGES = 2  # Revoke privileges from a user.
