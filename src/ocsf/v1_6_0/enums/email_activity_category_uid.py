"""The category unique identifier of the event. enumeration."""

from enum import IntEnum


class EmailActivityCategoryUid(IntEnum):
    """The category unique identifier of the event.

    See: https://schema.ocsf.io/1.6.0/data_types/email_activity_category_uid
    """

    UNCATEGORIZED = 0  #
