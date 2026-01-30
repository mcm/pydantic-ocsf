"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class DeviceConfigStateChangeActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.7.0/data_types/device_config_state_change_activity_id
    """

    LOG = 1  # The discovered information is via a log.
    COLLECT = 2  # The discovered information is via a collection process.
