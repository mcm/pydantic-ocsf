"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class OsintInventoryInfoActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.7.0/data_types/osint_inventory_info_activity_id
    """

    LOG = 1  # The discovered information is via a log.
    COLLECT = 2  # The discovered information is via a collection process.
