"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class MemoryActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.2.0/data_types/memory_activity_activity_id
    """

    ALLOCATE_PAGE = 1  #
    MODIFY_PAGE = 2  #
    DELETE_PAGE = 3  #
    BUFFER_OVERFLOW = 4  #
    DISABLE_DEP = 5  # Data Execution Permission
    ENABLE_DEP = 6  # Data Execution Permission
    READ = 7  # Read (Example: <code>ReadProcessMemory</code>)
    WRITE = 8  # Write (Example: <code>WriteProcessMemory</code>)
