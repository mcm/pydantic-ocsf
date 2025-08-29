from datetime import datetime
from enum import Enum, property as enum_property
from typing import Any, ClassVar

from pydantic import AnyUrl

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


class StateId(Enum):
    UNKNOWN = 0
    PENDING = 1
    ACTIVE = 2
    FAILED = 3
    DELETED = 4
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return StateId[obj]
        else:
            return StateId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "PENDING": "Pending",
            "ACTIVE": "Active",
            "FAILED": "Failed",
            "DELETED": "Deleted",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Scim(Object):
    schema_name: ClassVar[str] = "scim"

    # Recommended
    name: str | None = None
    scim_group_schema: dict[str, Any] | None = None
    scim_user_schema: dict[str, Any] | None = None
    uid: str | None = None
    version: str | None = None

    # Optional
    auth_protocol: str | None = None
    auth_protocol_id: AuthProtocolId | None = None
    created_time: datetime | None = None
    error_message: str | None = None
    is_group_provisioning_enabled: bool | None = None
    is_user_provisioning_enabled: bool | None = None
    last_run_time: datetime | None = None
    modified_time: datetime | None = None
    protocol_name: str | None = None
    rate_limit: int | None = None
    state: str | None = None
    state_id: StateId | None = None
    uid_alt: str | None = None
    url_string: AnyUrl | None = None
    vendor_name: str | None = None
