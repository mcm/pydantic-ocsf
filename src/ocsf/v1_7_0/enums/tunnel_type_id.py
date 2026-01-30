"""The normalized tunnel type ID. enumeration."""

from enum import IntEnum


class TunnelTypeId(IntEnum):
    """The normalized tunnel type ID.

    See: https://schema.ocsf.io/1.7.0/data_types/tunnel_type_id
    """

    UNKNOWN = 0  #
    SPLIT_TUNNEL = 1  #
    FULL_TUNNEL = 2  #
    OTHER = 99  #
