"""The category unique identifier of the event. enumeration."""

from enum import IntEnum


class ProcessQueryCategoryUid(IntEnum):
    """The category unique identifier of the event.

    See: https://schema.ocsf.io/1.6.0/data_types/process_query_category_uid
    """

    UNCATEGORIZED = 0  #
