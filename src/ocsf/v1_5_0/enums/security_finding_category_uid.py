"""The category unique identifier of the event. enumeration."""

from enum import IntEnum


class SecurityFindingCategoryUid(IntEnum):
    """The category unique identifier of the event.

    See: https://schema.ocsf.io/1.5.0/data_types/security_finding_category_uid
    """

    UNCATEGORIZED = 0  #
