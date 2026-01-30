"""The current security level of the entity enumeration."""

from enum import IntEnum


class DeviceConfigStateChangeSecurityLevelId(IntEnum):
    """The current security level of the entity

    See: https://schema.ocsf.io/1.5.0/data_types/device_config_state_change_security_level_id
    """

    UNKNOWN = 0  #
    SECURE = 1  #
    AT_RISK = 2  #
    COMPROMISED = 3  #
    OTHER = 99  # The security level is not mapped. See the <code>security_level</code> attribute, which contains data source specific values.
