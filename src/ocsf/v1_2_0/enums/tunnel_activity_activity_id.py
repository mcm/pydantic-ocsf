"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class TunnelActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.2.0/data_types/tunnel_activity_activity_id
    """

    UNKNOWN = 0  # The event activity is unknown.
    OPEN = 1  # Open a tunnel.
    CLOSE = 2  # Close a tunnel.
    RENEW = 3  # Renew a tunnel.
    OTHER = 99  # The event activity is not mapped. See the <code>activity_name</code> attribute, which contains a data source specific value.
