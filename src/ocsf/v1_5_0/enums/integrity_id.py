"""The normalized identifier of the process integrity level (Windows only). enumeration."""

from enum import IntEnum


class IntegrityId(IntEnum):
    """The normalized identifier of the process integrity level (Windows only).

    See: https://schema.ocsf.io/1.5.0/data_types/integrity_id
    """

    UNKNOWN = 0  # The integrity level is unknown.
    UNTRUSTED = 1  #
    LOW = 2  #
    MEDIUM = 3  #
    HIGH = 4  #
    SYSTEM = 5  #
    PROTECTED = 6  #
    OTHER = 99  # The integrity level is not mapped. See the <code>integrity</code> attribute, which contains a data source specific value.
