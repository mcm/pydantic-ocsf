from enum import Enum, property as enum_property
from typing import Any, ClassVar, TYPE_CHECKING

from pydantic import EmailStr, model_validator

from ocsf.objects._entity import Entity
from ocsf.objects.account import Account
from ocsf.objects.group import Group
from ocsf.objects.organization import Organization
from ocsf.objects.programmatic_credential import ProgrammaticCredential

if TYPE_CHECKING:
    from ocsf.objects.ldap_person import LdapPerson


class RiskLevelId(Enum):
    INFO = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return RiskLevelId[obj]
        else:
            return RiskLevelId(obj)

    @enum_property
    def name(self):
        name_map = {
            "INFO": "Info",
            "LOW": "Low",
            "MEDIUM": "Medium",
            "HIGH": "High",
            "CRITICAL": "Critical",
            "OTHER": "Other",
        }
        return name_map[super().name]


class TypeId(Enum):
    UNKNOWN = 0
    USER = 1
    ADMIN = 2
    SYSTEM = 3
    SERVICE = 4
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return TypeId[obj]
        else:
            return TypeId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "USER": "User",
            "ADMIN": "Admin",
            "SYSTEM": "System",
            "SERVICE": "Service",
            "OTHER": "Other",
        }
        return name_map[super().name]


class User(Entity):
    schema_name: ClassVar[str] = "user"

    # Recommended
    has_mfa: bool | None = None
    name: str | None = None
    type_id: TypeId | None = None
    uid: str | None = None

    # Optional
    account: Account | None = None
    credential_uid: str | None = None
    display_name: str | None = None
    domain: str | None = None
    email_addr: EmailStr | None = None
    forward_addr: EmailStr | None = None
    full_name: str | None = None
    groups: list[Group] | None = None
    ldap_person: "LdapPerson | None" = None
    org: Organization | None = None
    phone_number: str | None = None
    programmatic_credentials: list[ProgrammaticCredential] | None = None
    risk_level: str | None = None
    risk_level_id: RiskLevelId | None = None
    risk_score: int | None = None
    type_: str | None = None
    uid_alt: str | None = None

    @model_validator(mode="after")
    def validate_at_least_one(self):
        if all(getattr(self, field) is None for field in ["account", "name", "uid"]):
            raise ValueError("At least one of `account`, `name`, `uid` must be provided")
        return self
