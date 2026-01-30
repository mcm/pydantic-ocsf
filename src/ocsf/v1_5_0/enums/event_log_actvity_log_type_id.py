"""The normalized log type identifier. enumeration."""

from enum import IntEnum


class EventLogActvityLogTypeId(IntEnum):
    """The normalized log type identifier.

    See: https://schema.ocsf.io/1.5.0/data_types/event_log_actvity_log_type_id
    """

    UNKNOWN = 0  # The log type is unknown.
    OS = 1  # The log type is an Operating System log.
    APPLICATION = 2  # The log type is an Application log.
    OTHER = 99  # The log type is not mapped. See the <code>log_type</code> attribute, which contains a data source specific value.
