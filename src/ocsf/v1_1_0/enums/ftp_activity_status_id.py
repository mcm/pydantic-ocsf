"""The normalized identifier of the event status. enumeration."""

from enum import IntEnum


class FtpActivityStatusId(IntEnum):
    """The normalized identifier of the event status.

    See: https://schema.ocsf.io/1.1.0/data_types/ftp_activity_status_id
    """

    UNKNOWN = 0  # The status is unknown.
    SUCCESS = 1  #
    FAILURE = 2  #
    OTHER = 99  # The event status is not mapped. See the <code>status</code> attribute, which contains a data source specific value.
