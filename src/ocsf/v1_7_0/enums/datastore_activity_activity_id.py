"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class DatastoreActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.7.0/data_types/datastore_activity_activity_id
    """

    READ = 1  # The 'Read' activity involves accessing specific data record details.
    UPDATE = 2  # The 'Update' activity pertains to modifying specific data record details.
    CONNECT = 3  # The 'Connect' activity involves establishing a connection to the datastore.
    QUERY = 4  # The 'Query' activity involves retrieving a filtered subset of data based on specific criteria.
    WRITE = 5  # The 'Write' activity involves writing specific data record details.
    CREATE = 6  # The 'Create' activity involves generating new data record details.
    DELETE = 7  # The 'Delete' activity involves removing specific data record details.
    LIST = 8  # The 'List' activity provides an overview of existing data records.
    ENCRYPT = (
        9  # The 'Encrypt' activity involves securing data by encrypting a specific data record.
    )
    DECRYPT = (
        10  # The 'Decrypt' activity involves converting encrypted data back to its original format.
    )
