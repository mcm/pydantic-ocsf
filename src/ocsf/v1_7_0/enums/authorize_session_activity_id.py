"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class AuthorizeSessionActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.7.0/data_types/authorize_session_activity_id
    """

    ASSIGN_PRIVILEGES = 1  # Assign special privileges to a new logon.
    ASSIGN_GROUPS = 2  # Assign special groups to a new logon.
