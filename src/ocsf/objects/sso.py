from datetime import datetime
from enum import Enum, property as enum_property
from typing import Any, ClassVar

from pydantic import AnyUrl

from ocsf.objects.certificate import Certificate
from ocsf.objects.object import Object


class AuthProtocolId(Enum):
    UNKNOWN = 0
    NTLM = 1
    KERBEROS = 2
    DIGEST = 3
    OPENID = 4
    SAML = 5
    OAUTH_2_0 = 6
    PAP = 7
    CHAP = 8
    EAP = 9
    RADIUS = 10
    BASIC_AUTHENTICATION = 11
    LDAP = 12
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return AuthProtocolId[obj]
        else:
            return AuthProtocolId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "NTLM": "NTLM",
            "KERBEROS": "Kerberos",
            "DIGEST": "Digest",
            "OPENID": "OpenID",
            "SAML": "SAML",
            "OAUTH_2_0": "OAUTH 2.0",
            "PAP": "PAP",
            "CHAP": "CHAP",
            "EAP": "EAP",
            "RADIUS": "RADIUS",
            "BASIC_AUTHENTICATION": "Basic Authentication",
            "LDAP": "LDAP",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Sso(Object):
    schema_name: ClassVar[str] = "sso"

    # Recommended
    certificate: Certificate | None = None
    name: str | None = None
    uid: str | None = None

    # Optional
    auth_protocol: str | None = None
    auth_protocol_id: AuthProtocolId | None = None
    created_time: datetime | None = None
    duration_mins: int | None = None
    idle_timeout: int | None = None
    login_endpoint: AnyUrl | None = None
    logout_endpoint: AnyUrl | None = None
    metadata_endpoint: AnyUrl | None = None
    modified_time: datetime | None = None
    protocol_name: str | None = None
    scopes: list[str] | None = None
    vendor_name: str | None = None
