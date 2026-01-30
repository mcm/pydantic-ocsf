"""The category unique identifier of the event. enumeration."""

from enum import IntEnum


class UserAccessCategoryUid(IntEnum):
    """The category unique identifier of the event.

    See: https://schema.ocsf.io/1.7.0/data_types/user_access_category_uid
    """

    UNCATEGORIZED = 0  #
