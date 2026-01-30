"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class ModuleQueryActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.2.0/data_types/module_query_activity_id
    """

    QUERY = 1  # The discovered results are via a query request.
