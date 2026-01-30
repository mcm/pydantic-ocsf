"""The normalized status identifier of the compliance check. enumeration."""

from enum import IntEnum


class CheckStatusId(IntEnum):
    """The normalized status identifier of the compliance check.

    See: https://schema.ocsf.io/1.5.0/data_types/check_status_id
    """

    UNKNOWN = 0  # The status is unknown.
    PASS = 1  # The compliance check passed for all the evaluated resources.
    WARNING = 2  # The compliance check did not yield a result due to missing information.
    FAIL = 3  # The compliance check failed for at least one of the evaluated resources.
    OTHER = 99  # The event status is not mapped. See the <code>status</code> attribute, which contains a data source specific value.
