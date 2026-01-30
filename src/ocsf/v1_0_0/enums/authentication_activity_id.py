"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class AuthenticationActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.0.0/data_types/authentication_activity_id
    """

    LOGON = 1  # A new logon session was requested.
    LOGOFF = 2  # A logon session was terminated and no longer exists.
    AUTHENTICATION_TICKET = 3  # A Kerberos authentication ticket (TGT) was requested.
    SERVICE_TICKET = 4  # A Kerberos service ticket was requested.
