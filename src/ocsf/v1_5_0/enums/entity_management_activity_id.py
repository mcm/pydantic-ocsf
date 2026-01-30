"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class EntityManagementActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.5.0/data_types/entity_management_activity_id
    """

    CREATE = 1  # Create a new managed entity.
    READ = 2  # Read an existing managed entity.
    UPDATE = 3  # Update an existing managed entity.
    DELETE = 4  # Delete a managed entity.
    MOVE = 5  # Move or rename an existing managed entity.
    ENROLL = 6  # Enroll an existing managed entity.
    UNENROLL = 7  # Unenroll an existing managed entity.
    ENABLE = 8  # Enable an existing managed entity. Note: This is typically regarded as a semi-permanent, editor visible, syncable change.
    DISABLE = 9  # Disable an existing managed entity. Note: This is typically regarded as a semi-permanent, editor visible, syncable change.
    ACTIVATE = 10  # Activate an existing managed entity. Note: This is a typically regarded as a transient change, a change of state of the engine.
    DEACTIVATE = 11  # Deactivate an existing managed entity. Note: This is a typically regarded as a transient change, a change of state of the engine.
    SUSPEND = 12  # Suspend an existing managed entity.
    RESUME = 13  # Resume (unsuspend) an existing managed entity.
