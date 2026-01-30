"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class StartupItemQueryActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.7.0/data_types/startup_item_query_activity_id
    """

    QUERY = 1  # The discovered results are via a query request.
