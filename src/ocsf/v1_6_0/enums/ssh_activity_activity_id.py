"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class SshActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.6.0/data_types/ssh_activity_activity_id
    """

    OPEN = 1  # A new network connection was opened.
    CLOSE = 2  # The network connection was closed.
    RESET = 3  # The network connection was abnormally terminated or closed by a middle device like firewalls.
    FAIL = 4  # The network connection failed. For example a connection timeout or no route to host.
    REFUSE = 5  # The network connection was refused. For example an attempt to connect to a server port which is not open.
    TRAFFIC = 6  # Network traffic report.
    LISTEN = 7  # A network endpoint began listening for new network connections.
