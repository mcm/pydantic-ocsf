"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class DiscoveryResultActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.6.0/data_types/discovery_result_activity_id
    """

    QUERY = 1  # The discovered results are via a query request.
