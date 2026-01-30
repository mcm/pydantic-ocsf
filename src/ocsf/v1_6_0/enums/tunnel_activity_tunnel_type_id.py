"""The normalized tunnel type ID. enumeration."""

from enum import IntEnum


class TunnelActivityTunnelTypeId(IntEnum):
    """The normalized tunnel type ID.

    See: https://schema.ocsf.io/1.6.0/data_types/tunnel_activity_tunnel_type_id
    """

    UNKNOWN = 0  #
    SPLIT_TUNNEL = 1  #
    FULL_TUNNEL = 2  #
    OTHER = 99  #
