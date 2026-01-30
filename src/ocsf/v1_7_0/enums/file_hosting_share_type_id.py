"""The normalized identifier of the share type. enumeration."""

from enum import IntEnum


class FileHostingShareTypeId(IntEnum):
    """The normalized identifier of the share type.

    See: https://schema.ocsf.io/1.7.0/data_types/file_hosting_share_type_id
    """

    UNKNOWN = 0  # The share type is unknown.
    FILE = 1  #
    PIPE = 2  #
    PRINT = 3  #
    OTHER = 99  # The share type is not mapped. See the <code>share_type</code> attribute, which contains a data source specific value.
