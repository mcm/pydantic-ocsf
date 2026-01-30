"""The normalized status identifier of the classification job. enumeration."""

from enum import IntEnum


class DataSecurityStatusId(IntEnum):
    """The normalized status identifier of the classification job.

    See: https://schema.ocsf.io/1.5.0/data_types/data_security_status_id
    """

    UNKNOWN = 0  #
    COMPLETE = 1  # The classification job completed for the evaluated resource.
    PARTIAL = 2  # The classification job partially completed for the evaluated resource.
    FAIL = 3  # The classification job failed for the evaluated resource.
    OTHER = 99  # The classification job type id is not mapped.
