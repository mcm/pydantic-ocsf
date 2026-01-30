"""The previous security level of the entity enumeration."""

from enum import IntEnum


class PrevSecurityLevelId(IntEnum):
    """The previous security level of the entity

    See: https://schema.ocsf.io/1.5.0/data_types/prev_security_level_id
    """

    UNKNOWN = 0  #
    SECURE = 1  #
    AT_RISK = 2  #
    COMPROMISED = 3  #
    OTHER = 99  # The security level is not mapped. See the <code>prev_security_level</code> attribute, which contains data source specific values.
