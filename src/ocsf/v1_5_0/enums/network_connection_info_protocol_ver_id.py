"""The Internet Protocol version identifier. enumeration."""

from enum import IntEnum


class NetworkConnectionInfoProtocolVerId(IntEnum):
    """The Internet Protocol version identifier.

    See: https://schema.ocsf.io/1.5.0/data_types/network_connection_info_protocol_ver_id
    """

    UNKNOWN = 0  #
    INTERNET_PROTOCOL_VERSION_4__IPV4_ = 4  #
    INTERNET_PROTOCOL_VERSION_6__IPV6_ = 6  #
    OTHER = 99  #
