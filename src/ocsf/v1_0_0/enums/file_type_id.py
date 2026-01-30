"""The file type ID. enumeration."""

from enum import IntEnum


class FileTypeId(IntEnum):
    """The file type ID.

    See: https://schema.ocsf.io/1.0.0/data_types/file_type_id
    """

    UNKNOWN = 0  #
    REGULAR_FILE = 1  #
    FOLDER = 2  #
    CHARACTER_DEVICE = 3  #
    BLOCK_DEVICE = 4  #
    LOCAL_SOCKET = 5  #
    NAMED_PIPE = 6  #
    SYMBOLIC_LINK = 7  #
    OTHER = 99  #
