"""The normalized identifier of the account switch method. enumeration."""

from enum import IntEnum


class AuthenticationAccountSwitchTypeId(IntEnum):
    """The normalized identifier of the account switch method.

    See: https://schema.ocsf.io/1.6.0/data_types/authentication_account_switch_type_id
    """

    UNKNOWN = 0  # The account switch type is unknown.
    SUBSTITUTE_USER = 1  # A utility like <code>sudo</code>, <code>su</code>, or equivalent was used to perform actions in the context of another user.
    IMPERSONATE = 2  # An API like <code>ImpersonateLoggedOnUser()</code> or equivalent was used to perform actions in the context of another user.
    OTHER = 99  # The account switch type is not mapped. See the <code>account_switch_type</code> attribute, which contains a data source specific value.
