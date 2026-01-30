"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class RdpActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.6.0/data_types/rdp_activity_activity_id
    """

    INITIAL_REQUEST = 1  # The initial RDP request.
    INITIAL_RESPONSE = 2  # The initial RDP response.
    CONNECT_REQUEST = 3  # An RDP connection request.
    CONNECT_RESPONSE = 4  # An RDP connection response.
    TLS_HANDSHAKE = 5  # The TLS handshake.
    TRAFFIC = 6  # Network traffic report.
    DISCONNECT = 7  # An RDP connection disconnect.
    RECONNECT = 8  # An RDP connection reconnect.
