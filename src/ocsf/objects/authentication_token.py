from datetime import datetime
from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects.encryption_details import EncryptionDetails
from ocsf.objects.object import Object


class TypeId(Enum):
    UNKNOWN = 0
    TICKET_GRANTING_TICKET = 1
    SERVICE_TICKET = 2
    IDENTITY_TOKEN = 3
    REFRESH_TOKEN = 4
    SAML_ASSERTION = 5
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
            "TICKET_GRANTING_TICKET": "Ticket Granting Ticket",
            "SERVICE_TICKET": "Service Ticket",
            "IDENTITY_TOKEN": "Identity Token",
            "REFRESH_TOKEN": "Refresh Token",
            "SAML_ASSERTION": "SAML Assertion",
            "OTHER": "Other",
        }
        return name_map[super().name]


class AuthenticationToken(Object):
    schema_name: ClassVar[str] = "authentication_token"

    # Recommended
    created_time: datetime | None = None
    encryption_details: EncryptionDetails | None = None
    kerberos_flags: str | None = None
    type_: str | None = None
    type_id: TypeId | None = None

    # Optional
    expiration_time: datetime | None = None
    is_renewable: bool | None = None
