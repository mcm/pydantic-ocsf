"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class ApiActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.0.0/data_types/api_activity_activity_id
    """

    CREATE = 1  # The API call in the event pertains to a 'create' activity.
    READ = 2  # The API call in the event pertains to a 'read' activity.
    UPDATE = 3  # The API call in the event pertains to a 'update' activity.
    DELETE = 4  # The API call in the event pertains to a 'delete' activity.
