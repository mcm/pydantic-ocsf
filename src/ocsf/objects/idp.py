from enum import Enum, property as enum_property
from typing import Any, ClassVar

from pydantic import AnyUrl

from ocsf.objects._entity import Entity
from ocsf.objects.auth_factor import AuthFactor
from ocsf.objects.fingerprint import Fingerprint
from ocsf.objects.scim import Scim
from ocsf.objects.sso import Sso


class StateId(Enum):
    UNKNOWN = 0
    ACTIVE = 1
    SUSPENDED = 2
    DEPRECATED = 3
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
            "ACTIVE": "Active",
            "SUSPENDED": "Suspended",
            "DEPRECATED": "Deprecated",
            "DELETED": "Deleted",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Idp(Entity):
    schema_name: ClassVar[str] = "idp"

    # Recommended
    name: str | None = None
    uid: str | None = None

    # Optional
    auth_factors: list[AuthFactor] | None = None
    domain: str | None = None
    fingerprint: Fingerprint | None = None
    has_mfa: bool | None = None
    issuer: str | None = None
    protocol_name: str | None = None
    scim: Scim | None = None
    sso: Sso | None = None
    state: str | None = None
    state_id: StateId | None = None
    tenant_uid: str | None = None
    url_string: AnyUrl | None = None
