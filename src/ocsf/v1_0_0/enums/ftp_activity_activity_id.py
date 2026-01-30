"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class FtpActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.0.0/data_types/ftp_activity_activity_id
    """

    PUT = 1  # File upload to the FTP or SFTP site.
    GET = 2  # File download from the FTP or SFTP site.
    POLL = 3  # Poll directory for specific file(s) or folder(s) at the FTP or SFTP site location.
    DELETE = 4  # Delete file(s) from the FTP or SFTP site.
    RENAME = 5  # Rename the file(s) in the FTP or SFTP site.
    LIST = 6  # List files in a specified directory.
