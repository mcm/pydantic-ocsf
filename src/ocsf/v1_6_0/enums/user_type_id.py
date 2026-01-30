"""The account type identifier. enumeration."""

from enum import IntEnum


class UserTypeId(IntEnum):
    """The account type identifier.

    See: https://schema.ocsf.io/1.6.0/data_types/user_type_id
    """

    UNKNOWN = 0  #
    USER = 1  # Regular user account.
    ADMIN = 2  # Admin/root user account.
    SYSTEM = (
        3  # System account. For example, Windows computer accounts with a trailing dollar sign ($).
    )
    SERVICE = 4  # Service account. For example, Windows service account.
    OTHER = 99  #
