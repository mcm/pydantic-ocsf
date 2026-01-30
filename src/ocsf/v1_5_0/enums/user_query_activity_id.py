"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class UserQueryActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.5.0/data_types/user_query_activity_id
    """

    QUERY = 1  # The discovered results are via a query request.
