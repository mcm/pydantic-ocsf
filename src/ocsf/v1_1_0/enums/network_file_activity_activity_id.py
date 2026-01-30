"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class NetworkFileActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.1.0/data_types/network_file_activity_activity_id
    """

    UPLOAD = 1  # Upload a file.
    DOWNLOAD = 2  # Download a file.
    UPDATE = 3  # Update a file.
    DELETE = 4  # Delete a file.
    RENAME = 5  # Rename a file.
    COPY = 6  # Copy a file.
    MOVE = 7  # Move a file.
    RESTORE = 8  # Restore a file.
    PREVIEW = 9  # Preview a file.
    LOCK = 10  # Lock a file.
    UNLOCK = 11  # Unlock a file.
    SHARE = 12  # Share a file.
    UNSHARE = 13  # Unshare a file.
    OPEN = 14  # Open a file.
    SYNC = 15  # Mark a file or folder to sync with a computer.
    UNSYNC = 16  # Mark a file or folder to not sync with a computer.
