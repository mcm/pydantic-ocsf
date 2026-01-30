"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class SmbActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.7.0/data_types/smb_activity_activity_id
    """

    FILE_SUPERSEDE = 1  # The event pertains to file superseded activity (overwritten if it exists and created if not).
    FILE_OPEN = 2  # The event pertains to file open activity (the file is opened if it exists and fails to open if it doesn't).
    FILE_CREATE = 3  # The event pertains to file creation activity (a file is created if it does not exist and fails if it does).
    FILE_OPEN_IF = 4  # The event pertains to file open activity (the file is opened if it exists and is created if it doesn't).
    FILE_OVERWRITE = 5  # The event pertains to file overwrite activity (the file is opened in a truncated form if it exists and fails if it doesn't).
    FILE_OVERWRITE_IF = 6  # The event pertains to file overwrite activity (the file is opened in a truncated form if it exists and created otherwise)
