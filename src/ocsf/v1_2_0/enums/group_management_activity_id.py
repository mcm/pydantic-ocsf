"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class GroupManagementActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.2.0/data_types/group_management_activity_id
    """

    ASSIGN_PRIVILEGES = 1  # Assign privileges to a group.
    REVOKE_PRIVILEGES = 2  # Revoke privileges from a group.
    ADD_USER = 3  # Add user to a group.
    REMOVE_USER = 4  # Remove user from a group.
    DELETE = 5  # A group was deleted.
    CREATE = 6  # A group was created.
