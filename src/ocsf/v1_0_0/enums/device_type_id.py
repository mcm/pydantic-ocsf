"""The device type ID. enumeration."""

from enum import IntEnum


class DeviceTypeId(IntEnum):
    """The device type ID.

    See: https://schema.ocsf.io/1.0.0/data_types/device_type_id
    """

    SERVER = 1  #
    DESKTOP = 2  #
    LAPTOP = 3  #
    TABLET = 4  #
    MOBILE = 5  #
    VIRTUAL = 6  #
    IOT = 7  #
    BROWSER = 8  #
