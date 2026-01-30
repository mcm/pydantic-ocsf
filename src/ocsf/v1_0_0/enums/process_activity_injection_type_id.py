"""The normalized identifier of the process injection method. enumeration."""

from enum import IntEnum


class ProcessActivityInjectionTypeId(IntEnum):
    """The normalized identifier of the process injection method.

    See: https://schema.ocsf.io/1.0.0/data_types/process_activity_injection_type_id
    """

    UNKNOWN = 0  #
    REMOTE_THREAD = 1  #
    LOAD_LIBRARY = 2  #
    OTHER = 99  #
