"""The normalized datastore resource type identifier. enumeration."""

from enum import IntEnum


class DatastoreActivityTypeId(IntEnum):
    """The normalized datastore resource type identifier.

    See: https://schema.ocsf.io/1.1.0/data_types/datastore_activity_type_id
    """

    UNKNOWN = 0  # The datastore resource type is unknown.
    DATABASE = 1  #
    DATABUCKET = 2  #
    TABLE = 3  #
    OTHER = 99  # The datastore resource type is not mapped.
