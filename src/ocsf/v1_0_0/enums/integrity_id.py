"""The normalized identifier of the process integrity level (Windows only). enumeration."""

from enum import IntEnum


class IntegrityId(IntEnum):
    """The normalized identifier of the process integrity level (Windows only).

    See: https://schema.ocsf.io/1.0.0/data_types/integrity_id
    """

    UNKNOWN = 0  #
    UNTRUSTED = 1  #
    LOW = 2  #
    MEDIUM = 3  #
    HIGH = 4  #
    SYSTEM = 5  #
    PROTECTED = 6  #
    OTHER = 99  #
