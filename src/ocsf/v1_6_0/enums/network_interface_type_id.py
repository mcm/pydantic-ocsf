"""The network interface type identifier. enumeration."""

from enum import IntEnum


class NetworkInterfaceTypeId(IntEnum):
    """The network interface type identifier.

    See: https://schema.ocsf.io/1.6.0/data_types/network_interface_type_id
    """

    UNKNOWN = 0  #
    WIRED = 1  #
    WIRELESS = 2  #
    MOBILE = 3  #
    TUNNEL = 4  #
    OTHER = 99  #
