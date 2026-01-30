"""The file type ID. Note the distinction between a <code>Regular File</code> and an <code>Executable File</code>. If the distinction is not known, or not indicated by the log, use <code>Regular File</code>. In this case, it should not be assumed that a Regular File is not executable. enumeration."""

from enum import IntEnum


class FileTypeId(IntEnum):
    """The file type ID. Note the distinction between a <code>Regular File</code> and an <code>Executable File</code>. If the distinction is not known, or not indicated by the log, use <code>Regular File</code>. In this case, it should not be assumed that a Regular File is not executable.

    See: https://schema.ocsf.io/1.6.0/data_types/file_type_id
    """

    UNKNOWN = 0  #
    REGULAR_FILE = 1  #
    FOLDER = 2  #
    CHARACTER_DEVICE = 3  #
    BLOCK_DEVICE = 4  #
    LOCAL_SOCKET = 5  #
    NAMED_PIPE = 6  #
    SYMBOLIC_LINK = 7  #
    EXECUTABLE_FILE = 8  #
    OTHER = 99  #
