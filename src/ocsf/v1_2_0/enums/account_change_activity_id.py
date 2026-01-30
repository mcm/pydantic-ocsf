"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class AccountChangeActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.2.0/data_types/account_change_activity_id
    """

    CREATE = 1  # A user/role was created.
    ENABLE = 2  # A user/role was enabled.
    PASSWORD_CHANGE = 3  # An attempt was made to change an account's password.
    PASSWORD_RESET = 4  # An attempt was made to reset an account's password.
    DISABLE = 5  # A user/role was disabled.
    DELETE = 6  # A user/role was deleted.
    ATTACH_POLICY = 7  # An IAM Policy was attached to a user/role.
    DETACH_POLICY = 8  # An IAM Policy was detached from a user/role.
    LOCK = 9  # A user account was locked out.
    MFA_FACTOR_ENABLE = 10  # An authentication factor was enabled for an account.
    MFA_FACTOR_DISABLE = 11  # An authentication factor was disabled for an account.
