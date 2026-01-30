"""The normalized identifier of the authentication protocol used to create the user session. enumeration."""

from enum import IntEnum


class AuthenticationAuthProtocolId(IntEnum):
    """The normalized identifier of the authentication protocol used to create the user session.

    See: https://schema.ocsf.io/1.2.0/data_types/authentication_auth_protocol_id
    """

    UNKNOWN = 0  # The authentication protocol is unknown.
    NTLM = 1  #
    KERBEROS = 2  #
    DIGEST = 3  #
    OPENID = 4  #
    SAML = 5  #
    OAUTH_2_0 = 6  #
    PAP = 7  #
    CHAP = 8  #
    EAP = 9  #
    RADIUS = 10  #
    OTHER = 99  # The authentication protocol is not mapped. See the <code>auth_protocol</code> attribute, which contains a data source specific value.
