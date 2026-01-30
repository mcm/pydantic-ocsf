"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class DiscoveryActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.1.0/data_types/discovery_activity_id
    """

    LOG = 1  # The discovered information is via a log.
    COLLECT = 2  # The discovered information is via a collection process.
