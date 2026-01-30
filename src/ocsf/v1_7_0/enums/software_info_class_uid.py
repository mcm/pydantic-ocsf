"""The unique identifier of a class. A class describes the attributes available in an event. enumeration."""

from enum import IntEnum


class SoftwareInfoClassUid(IntEnum):
    """The unique identifier of a class. A class describes the attributes available in an event.

    See: https://schema.ocsf.io/1.7.0/data_types/software_info_class_uid
    """

    BASE_EVENT = 0  #
