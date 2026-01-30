"""The category unique identifier of the event. enumeration."""

from enum import IntEnum


class DhcpActivityCategoryUid(IntEnum):
    """The category unique identifier of the event.

    See: https://schema.ocsf.io/1.7.0/data_types/dhcp_activity_category_uid
    """

    UNCATEGORIZED = 0  #
