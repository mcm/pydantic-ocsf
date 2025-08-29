from enum import Enum, property as enum_property
from typing import Any, ClassVar

from pydantic import model_validator

from ocsf.events.iam.iam import IAM
from ocsf.objects.auth_factor import AuthFactor
from ocsf.objects.authentication_token import AuthenticationToken
from ocsf.objects.certificate import Certificate
from ocsf.objects.network_endpoint import NetworkEndpoint
from ocsf.objects.process import Process
from ocsf.objects.service import Service
from ocsf.objects.session import Session
from ocsf.objects.user import User


class AccountSwitchTypeId(Enum):
    UNKNOWN = 0
    SUBSTITUTE_USER = 1
    IMPERSONATE = 2
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return AccountSwitchTypeId[obj]
        else:
            return AccountSwitchTypeId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "SUBSTITUTE_USER": "Substitute User",
            "IMPERSONATE": "Impersonate",
            "OTHER": "Other",
        }
        return name_map[super().name]


class ActivityId(Enum):
    UNKNOWN = 0
    LOGON = 1
    LOGOFF = 2
    AUTHENTICATION_TICKET = 3
    SERVICE_TICKET_REQUEST = 4
    SERVICE_TICKET_RENEW = 5
    PREAUTH = 6
    ACCOUNT_SWITCH = 7
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return ActivityId[obj]
        else:
            return ActivityId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "LOGON": "Logon",
            "LOGOFF": "Logoff",
            "AUTHENTICATION_TICKET": "Authentication Ticket",
            "SERVICE_TICKET_REQUEST": "Service Ticket Request",
            "SERVICE_TICKET_RENEW": "Service Ticket Renew",
            "PREAUTH": "Preauth",
            "ACCOUNT_SWITCH": "Account Switch",
            "OTHER": "Other",
        }
        return name_map[super().name]


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


class LogonTypeId(Enum):
    UNKNOWN = 0
    SYSTEM = 1
    INTERACTIVE = 2
    NETWORK = 3
    BATCH = 4
    OS_SERVICE = 5
    UNLOCK = 7
    NETWORK_CLEARTEXT = 8
    NEW_CREDENTIALS = 9
    REMOTE_INTERACTIVE = 10
    CACHED_INTERACTIVE = 11
    CACHED_REMOTE_INTERACTIVE = 12
    CACHED_UNLOCK = 13
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return LogonTypeId[obj]
        else:
            return LogonTypeId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "SYSTEM": "System",
            "INTERACTIVE": "Interactive",
            "NETWORK": "Network",
            "BATCH": "Batch",
            "OS_SERVICE": "OS Service",
            "UNLOCK": "Unlock",
            "NETWORK_CLEARTEXT": "Network Cleartext",
            "NEW_CREDENTIALS": "New Credentials",
            "REMOTE_INTERACTIVE": "Remote Interactive",
            "CACHED_INTERACTIVE": "Cached Interactive",
            "CACHED_REMOTE_INTERACTIVE": "Cached Remote Interactive",
            "CACHED_UNLOCK": "Cached Unlock",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Authentication(IAM):
    schema_name: ClassVar[str] = "authentication"
    class_id: int = 3002
    class_name: str = "Authentication"

    # Required
    activity_id: ActivityId
    user: User

    # Recommended
    account_switch_type: str | None = None
    account_switch_type_id: AccountSwitchTypeId | None = None
    auth_protocol: str | None = None
    auth_protocol_id: AuthProtocolId | None = None
    certificate: Certificate | None = None
    dst_endpoint: NetworkEndpoint | None = None
    is_mfa: bool | None = None
    is_remote: bool | None = None
    logon_type: str | None = None
    logon_type_id: LogonTypeId | None = None
    service: Service | None = None
    session: Session | None = None
    status_detail: str | None = None

    # Optional
    auth_factors: list[AuthFactor] | None = None
    authentication_token: AuthenticationToken | None = None
    is_cleartext: bool | None = None
    is_new_logon: bool | None = None
    logon_process: Process | None = None

    @model_validator(mode="after")
    def validate_at_least_one(self):
        if all(getattr(self, field) is None for field in ["service", "dst_endpoint"]):
            raise ValueError("At least one of `service`, `dst_endpoint` must be provided")
        return self
