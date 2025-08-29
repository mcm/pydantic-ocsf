from enum import Enum, property as enum_property
from typing import Any, ClassVar

from pydantic import EmailStr

from ocsf.objects.location import Location
from ocsf.objects.object import Object


class TypeId(Enum):
    UNKNOWN = 0
    REGISTRANT = 1
    ADMINISTRATIVE = 2
    TECHNICAL = 3
    BILLING = 4
    ABUSE = 5
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
            "REGISTRANT": "Registrant",
            "ADMINISTRATIVE": "Administrative",
            "TECHNICAL": "Technical",
            "BILLING": "Billing",
            "ABUSE": "Abuse",
            "OTHER": "Other",
        }
        return name_map[super().name]


class DomainContact(Object):
    schema_name: ClassVar[str] = "domain_contact"

    # Required
    type_id: TypeId

    # Recommended
    email_addr: EmailStr | None = None
    location: Location | None = None

    # Optional
    name: str | None = None
    phone_number: str | None = None
    type_: str | None = None
    uid: str | None = None
