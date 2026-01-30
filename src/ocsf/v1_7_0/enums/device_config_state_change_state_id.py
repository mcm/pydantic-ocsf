"""The Config Change State of the managed entity. enumeration."""

from enum import IntEnum


class DeviceConfigStateChangeStateId(IntEnum):
    """The Config Change State of the managed entity.

    See: https://schema.ocsf.io/1.7.0/data_types/device_config_state_change_state_id
    """

    UNKNOWN = 0  # The Config Change state is unknown.
    DISABLED = 1  # Config State Changed to Disabled.
    ENABLED = 2  # Config State Changed to Enabled.
    OTHER = 99  # The Config Change is not mapped. See the <code>state</code> attribute, which contains data source specific values.
