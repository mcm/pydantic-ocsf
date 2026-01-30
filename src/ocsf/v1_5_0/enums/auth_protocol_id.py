"""The normalized identifier of the authorization protocol used by the SCIM resource. enumeration."""

from enum import IntEnum


class AuthProtocolId(IntEnum):
    """The normalized identifier of the authorization protocol used by the SCIM resource.

    See: https://schema.ocsf.io/1.5.0/data_types/auth_protocol_id
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
    BASIC_AUTHENTICATION = 11  #
    LDAP = 12  #
    OTHER = 99  # The authentication protocol is not mapped. See the <code>auth_protocol</code> attribute, which contains a data source specific value.
