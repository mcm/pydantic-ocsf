"""The unique identifier of a class. A class describes the attributes available in an event. enumeration."""

from enum import IntEnum


class SecurityFindingClassUid(IntEnum):
    """The unique identifier of a class. A class describes the attributes available in an event.

    See: https://schema.ocsf.io/1.5.0/data_types/security_finding_class_uid
    """

    BASE_EVENT = 0  #
