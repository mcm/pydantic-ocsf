"""The normalized identifier of the Data Security Finding activity. enumeration."""

from enum import IntEnum


class DataSecurityFindingActivityId(IntEnum):
    """The normalized identifier of the Data Security Finding activity.

    See: https://schema.ocsf.io/1.6.0/data_types/data_security_finding_activity_id
    """

    CREATE = 1  # A new Data Security finding is created.
    UPDATE = 2  # An existing Data Security finding is updated with more information.
    CLOSE = 3  # An existing Data Security finding is closed, this can be due to any resolution (e.g., True Positive, False Positive, etc.).
    SUPPRESSED = 4  # An existing Data Security finding is suppressed due to inaccurate detection techniques or a known true negative.
