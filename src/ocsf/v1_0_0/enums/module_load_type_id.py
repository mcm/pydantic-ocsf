"""The normalized identifier of the load type. It identifies how the module was loaded in memory. enumeration."""

from enum import IntEnum


class ModuleLoadTypeId(IntEnum):
    """The normalized identifier of the load type. It identifies how the module was loaded in memory.

    See: https://schema.ocsf.io/1.0.0/data_types/module_load_type_id
    """

    UNKNOWN = 0  #
    STANDARD = 1  # A normal module loaded by the normal windows loading mechanism i.e. LoadLibrary.
    NON_STANDARD = 2  # A module loaded in a way avoidant of normal windows procedures. i.e. Bootstrapped Loading/Manual Dll Loading.
    SHELLCODE = 3  # A raw module in process memory that is READWRITE_EXECUTE and had a thread started in its range.
    MAPPED = 4  # A memory mapped file, typically created with CreatefileMapping/MapViewOfFile.
    NONSTANDARD_BACKED = 5  # A module loaded in a non standard way. However, GetModuleFileName succeeds on this allocation.
    OTHER = 99  #
