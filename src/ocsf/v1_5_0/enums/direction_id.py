"""The normalized identifier of the direction of the initiated connection, traffic, or email. enumeration."""

from enum import IntEnum


class DirectionId(IntEnum):
    """The normalized identifier of the direction of the initiated connection, traffic, or email.

    See: https://schema.ocsf.io/1.5.0/data_types/direction_id
    """

    UNKNOWN = 0  # The connection direction is unknown.
    INBOUND = 1  # Inbound network connection. The connection was originated from the Internet or outside network, destined for services on the inside network.
    OUTBOUND = 2  # Outbound network connection. The connection was originated from inside the network, destined for services on the Internet or outside network.
    LATERAL = 3  # Lateral network connection. The connection was originated from inside the network, destined for services on the inside network.
    OTHER = 99  # The direction is not mapped. See the <code>direction</code> attribute, which contains a data source specific value.
