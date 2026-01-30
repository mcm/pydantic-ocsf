"""The observable value type identifier. enumeration."""

from enum import IntEnum


class ObservableTypeId(IntEnum):
    """The observable value type identifier.

    See: https://schema.ocsf.io/1.2.0/data_types/observable_type_id
    """

    UNKNOWN = 0  # Unknown observable data type.
    OTHER = 99  # The observable data type is not mapped. See the <code>type</code> attribute, which may contain data source specific value.
