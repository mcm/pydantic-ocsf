"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class PeripheralActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.7.0/data_types/peripheral_activity_activity_id
    """

    CONNECT = 1  # A peripheral device was connected to the system.
    DISCONNECT = 2  # A peripheral device was disconnected from the system.
    ENABLE = 3  # A peripheral device was enabled on the system.
    DISABLE = 4  # A peripheral device was disabled on the system.
    EJECT = 5  # A peripheral device was ejected from the system. This is typically used for removable media devices. Note: For <code>Mount</code> and <code>Unmount</code> events, see the <a target='_blank' href='file_activity'>File System Activity</a> event class.
