"""The normalized identifier of the event status. enumeration."""

from enum import IntEnum


class FileRemediationActivityStatusId(IntEnum):
    """The normalized identifier of the event status.

    See: https://schema.ocsf.io/1.6.0/data_types/file_remediation_activity_status_id
    """

    DOES_NOT_EXIST = 3  # The target of the remediation does not exist.
    PARTIAL = 4  # The remediation was partially completed.
    UNSUPPORTED = 5  # The remediation was not supported.
    ERROR = 6  # There was an error during the remediation process.
