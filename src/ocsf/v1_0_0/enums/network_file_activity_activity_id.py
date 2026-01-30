"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class NetworkFileActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.0.0/data_types/network_file_activity_activity_id
    """

    UPLOAD = 1  #
    DOWNLOAD = 2  #
    UPDATE = 3  #
    DELETE = 4  #
    RENAME = 5  #
    COPY = 6  #
    MOVE = 7  #
    RESTORE = 8  #
    PREVIEW = 9  #
    LOCK = 10  #
    UNLOCK = 11  #
    SHARE = 12  #
    UNSHARE = 13  #
    OPEN = 14  #
