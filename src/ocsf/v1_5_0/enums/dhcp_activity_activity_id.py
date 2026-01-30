"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class DhcpActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.5.0/data_types/dhcp_activity_activity_id
    """

    DISCOVER = 1  # DHCPDISCOVER
    OFFER = 2  # DHCPOFFER
    REQUEST = 3  # DHCPREQUEST
    DECLINE = 4  # DHCPDECLINE
    ACK = 5  # DHCPACK: The server accepts the request by sending the client a DHCP Acknowledgment message.
    NAK = 6  # DHCPNAK
    RELEASE = 7  # DHCPRELEASE: A DHCP client sends a DHCPRELEASE packet to the server to release the IP address and cancel any remaining lease.
    INFORM = 8  # DHCPINFORM
    EXPIRE = 9  # DHCPEXPIRE: A DHCP lease expired.
