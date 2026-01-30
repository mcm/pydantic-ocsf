"""The normalized identifier for the time span duration type. enumeration."""

from enum import IntEnum


class TimespanTypeId(IntEnum):
    """The normalized identifier for the time span duration type.

    See: https://schema.ocsf.io/1.5.0/data_types/timespan_type_id
    """

    UNKNOWN = 0  #
    MILLISECONDS = 1  #
    SECONDS = 2  #
    MINUTES = 3  #
    HOURS = 4  #
    DAYS = 5  #
    WEEKS = 6  #
    MONTHS = 7  #
    YEARS = 8  #
    TIME_INTERVAL = 9  # The <code>start_time</code> and <code>end_time</code> should be set.
    OTHER = 99  #
