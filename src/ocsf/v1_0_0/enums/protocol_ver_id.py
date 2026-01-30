"""The Internet Protocol version identifier. enumeration."""

from enum import IntEnum


class ProtocolVerId(IntEnum):
    """The Internet Protocol version identifier.

    See: https://schema.ocsf.io/1.0.0/data_types/protocol_ver_id
    """

    UNKNOWN = 0  #
    INTERNET_PROTOCOL_VERSION_4__IPV4_ = 4  #
    INTERNET_PROTOCOL_VERSION_6__IPV6_ = 6  #
    OTHER = 99  #
