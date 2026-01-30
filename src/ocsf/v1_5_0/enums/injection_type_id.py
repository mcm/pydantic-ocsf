"""The normalized identifier of the process injection method. enumeration."""

from enum import IntEnum


class InjectionTypeId(IntEnum):
    """The normalized identifier of the process injection method.

    See: https://schema.ocsf.io/1.5.0/data_types/injection_type_id
    """

    UNKNOWN = 0  # The injection type is unknown.
    REMOTE_THREAD = 1  #
    LOAD_LIBRARY = 2  #
    QUEUE_APC = 3  #
    OTHER = 99  # The injection type is not mapped. See the <code>injection_type</code> attribute, which contains a data source specific value.
