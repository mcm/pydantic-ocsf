"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class AccountChangeActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.7.0/data_types/account_change_activity_id
    """

    CREATE = 1  # A user/role was created.
    ENABLE = 2  # A user/role was enabled.
    PASSWORD_CHANGE = 3  # An attempt was made to change a user account's password.
    PASSWORD_RESET = 4  # An attempt was made to reset a user account's password.
    DISABLE = 5  # A user/role was disabled.
    DELETE = 6  # A user/role was deleted.
    ATTACH_POLICY = 7  # An IAM Policy was attached to a user/role.
    DETACH_POLICY = 8  # An IAM Policy was detached from a user/role.
    LOCK = 9  # A user account was locked out.
    MFA_FACTOR_ENABLE = 10  # One or more authentication factors were enabled for a user account.
    MFA_FACTOR_DISABLE = 11  # One or more authentication factors were disabled for a user account.
    UNLOCK = 12  # A user account was unlocked.
