"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class AuthenticationActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.6.0/data_types/authentication_activity_id
    """

    LOGON = 1  # A new logon session was requested.
    LOGOFF = 2  # A logon session was terminated and no longer exists.
    AUTHENTICATION_TICKET = 3  # A Kerberos authentication ticket (TGT) was requested.
    SERVICE_TICKET_REQUEST = 4  # A Kerberos service ticket was requested.
    SERVICE_TICKET_RENEW = 5  # A Kerberos service ticket was renewed.
    PREAUTH = 6  # A preauthentication stage was engaged.
    ACCOUNT_SWITCH = 7  # A utility or service switched the user account. See the <code>account_switch_type_id</code> attribute for more details.
