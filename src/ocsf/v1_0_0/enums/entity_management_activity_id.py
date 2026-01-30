"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class EntityManagementActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.0.0/data_types/entity_management_activity_id
    """

    CREATE = 1  #
    READ = 2  #
    UPDATE = 3  #
    DELETE = 4  #
