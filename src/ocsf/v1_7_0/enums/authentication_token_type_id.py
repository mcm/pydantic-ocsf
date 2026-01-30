"""The normalized authentication token type identifier. enumeration."""

from enum import IntEnum


class AuthenticationTokenTypeId(IntEnum):
    """The normalized authentication token type identifier.

    See: https://schema.ocsf.io/1.7.0/data_types/authentication_token_type_id
    """

    UNKNOWN = 0  # The Authentication token type is unknown.
    TICKET_GRANTING_TICKET = 1  # Ticket Granting Ticket (TGT) for Kerberos.
    SERVICE_TICKET = 2  # Service Ticket (ST) for Kerberos.
    IDENTITY_TOKEN = 3  # Identity (ID) Token for OIDC.
    REFRESH_TOKEN = 4  # Refresh Token for OIDC.
    SAML_ASSERTION = 5  # Authentication Assertion for SAML.
    OTHER = 99  #
