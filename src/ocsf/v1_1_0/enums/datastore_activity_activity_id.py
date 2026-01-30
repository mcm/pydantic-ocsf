"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class DatastoreActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.1.0/data_types/datastore_activity_activity_id
    """

    READ = 1  # The datastore activity in the event pertains to a 'Read' operation.
    UPDATE = 2  # The datastore activity in the event pertains to a 'Update' operation.
    CONNECT = 3  # The datastore activity in the event pertains to a 'Connect' operation.
    QUERY = 4  # The datastore activity in the event pertains to a 'Query' operation.
    WRITE = 5  # The datastore activity in the event pertains to a 'Write' operation.
    CREATE = 6  # The datastore activity in the event pertains to a 'Create' operation.
    DELETE = 7  # The datastore activity in the event pertains to a 'Delete' operation.
