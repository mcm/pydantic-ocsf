"""The normalized identifier of the event status. enumeration."""

from enum import IntEnum


class BaseEventStatusId(IntEnum):
    """The normalized identifier of the event status.

    See: https://schema.ocsf.io/1.0.0/data_types/base_event_status_id
    """

    UNKNOWN = 0  #
    SUCCESS = 1  #
    FAILURE = 2  #
    OTHER = 99  # The event status is not mapped. See the <code>status</code> attribute, which contains a data source specific value.
