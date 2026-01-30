"""The normalized identifier of the SSH authentication type. enumeration."""

from enum import IntEnum


class AuthTypeId(IntEnum):
    """The normalized identifier of the SSH authentication type.

    See: https://schema.ocsf.io/1.1.0/data_types/auth_type_id
    """

    UNKNOWN = 0  #
    CERTIFICATE_BASED = 1  # Authentication using digital certificates.
    GSSAPI = 2  # GSSAPI for centralized authentication.
    HOST_BASED = 3  # Authentication based on the client host's identity.
    KEYBOARD_INTERACTIVE = 4  # Multi-step, interactive authentication.
    PASSWORD = 5  # Password Authentication.
    PUBLIC_KEY = 6  # Paired public key authentication.
    OTHER = 99  #
