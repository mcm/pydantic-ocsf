"""The normalized logon type identifier. enumeration."""

from enum import IntEnum


class AuthenticationLogonTypeId(IntEnum):
    """The normalized logon type identifier.

    See: https://schema.ocsf.io/1.1.0/data_types/authentication_logon_type_id
    """

    SYSTEM = 0  # Used only by the System account, for example at system startup.
    INTERACTIVE = 2  # A local logon to device console.
    NETWORK = 3  # A user or device logged onto this device from the network.
    BATCH = 4  # A batch server logon, where processes may be executing on behalf of a user without their direct intervention.
    OS_SERVICE = 5  # A logon by a service or daemon that was started by the OS.
    UNLOCK = 7  # A user unlocked the device.
    NETWORK_CLEARTEXT = 8  # A user logged on to this device from the network. The user's password in the authentication package was not hashed.
    NEW_CREDENTIALS = 9  # A caller cloned its current token and specified new credentials for outbound connections. The new logon session has the same local identity, but uses different credentials for other network connections.
    REMOTE_INTERACTIVE = 10  # A remote logon using Terminal Services or remote desktop application.
    CACHED_INTERACTIVE = 11  # A user logged on to this device with network credentials that were stored locally on the device and the domain controller was not contacted to verify the credentials.
    CACHED_REMOTE_INTERACTIVE = (
        12  # Same as Remote Interactive. This is used for internal auditing.
    )
    CACHED_UNLOCK = 13  # Workstation logon.
    OTHER = 99  # The logon type is not mapped. See the <code>logon_type</code> attribute, which contains a data source specific value.
