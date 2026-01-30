"""The normalized identifier of the authentication protocol used to create the user session. enumeration."""

from enum import IntEnum


class AuthProtocolId(IntEnum):
    """The normalized identifier of the authentication protocol used to create the user session.

    See: https://schema.ocsf.io/1.0.0/data_types/auth_protocol_id
    """

    UNKNOWN = 0  #
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
    OTHER = 99  #
