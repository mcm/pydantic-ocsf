"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class KernelObjectQueryActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.6.0/data_types/kernel_object_query_activity_id
    """

    QUERY = 1  # The discovered results are via a query request.
