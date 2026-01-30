"""The normalized identifier of the database type. enumeration."""

from enum import IntEnum


class DatabaseTypeId(IntEnum):
    """The normalized identifier of the database type.

    See: https://schema.ocsf.io/1.1.0/data_types/database_type_id
    """

    UNKNOWN = 0  #
    RELATIONAL = 1  #
    NETWORK = 2  #
    CLOUD = 3  #
    CENTRALIZED = 4  #
    OPERATIONAL = 5  #
    NOSQL = 6  #
    OTHER = 99  #
