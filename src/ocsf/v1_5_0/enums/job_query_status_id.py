"""The normalized identifier of the event status. enumeration."""

from enum import IntEnum


class JobQueryStatusId(IntEnum):
    """The normalized identifier of the event status.

    See: https://schema.ocsf.io/1.5.0/data_types/job_query_status_id
    """

    UNKNOWN = 0  # The status is unknown.
    SUCCESS = 1  #
    FAILURE = 2  #
    OTHER = 99  # The event status is not mapped. See the <code>status</code> attribute, which contains a data source specific value.
