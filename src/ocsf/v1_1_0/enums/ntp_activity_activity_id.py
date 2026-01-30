"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class NtpActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.1.0/data_types/ntp_activity_activity_id
    """

    UNKNOWN = 0  # Not used in standard NTP implementations.
    SYMMETRIC_ACTIVE_EXCHANGE = 1  # Bidirectional time exchange between devices.
    SYMMETRIC_PASSIVE_RESPONSE = 2  # Device responds as a server to peers in symmetric active mode.
    CLIENT_SYNCHRONIZATION = 3  # NTP client, syncs with servers.
    SERVER_RESPONSE = 4  # Dedicated NTP time server, responds to clients.
    BROADCAST = 5  # Broadcast time info to network devices.
    CONTROL = 6  # Monitoring and control messaging.
    PRIVATE_USE_CASE = 7  # Reserved - Not defined in standard NTP specifications.
    OTHER = 99  # The event activity is not mapped.
