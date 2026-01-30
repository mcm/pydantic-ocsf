"""The unique identifier of a class. A class describes the attributes available in an event. enumeration."""

from enum import IntEnum


class BaseEventClassUid(IntEnum):
    """The unique identifier of a class. A class describes the attributes available in an event.

    See: https://schema.ocsf.io/1.6.0/data_types/base_event_class_uid
    """

    BASE_EVENT = 0  #
