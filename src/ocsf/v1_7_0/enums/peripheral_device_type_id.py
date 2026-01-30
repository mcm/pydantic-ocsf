"""The normalized peripheral device type ID. enumeration."""

from enum import IntEnum


class PeripheralDeviceTypeId(IntEnum):
    """The normalized peripheral device type ID.

    See: https://schema.ocsf.io/1.7.0/data_types/peripheral_device_type_id
    """

    UNKNOWN = 0  # The peripheral device type is unknown.
    EXTERNAL_STORAGE = 1  # The peripheral device is an external storage device.
    KEYBOARD = 2  # The peripheral device is a keyboard.
    MOUSE = 3  # The peripheral device is a mouse.
    PRINTER = 4  # The peripheral device is a printer.
    MONITOR = 5  # The peripheral device is a monitor.
    MICROPHONE = 6  # The peripheral device is a microphone.
    WEBCAM = 7  # The peripheral device is a webcam.
    OTHER = 99  # The peripheral device type is not mapped. See the <code>type</code> attribute which contains an event source specific value.
