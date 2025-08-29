from datetime import datetime
from enum import Enum, property as enum_property
from typing import Any, ClassVar

from pydantic import EmailStr, IPvAnyNetwork

from ocsf.objects.autonomous_system import AutonomousSystem
from ocsf.objects.domain_contact import DomainContact
from ocsf.objects.object import Object


class DnssecStatusId(Enum):
    UNKNOWN = 0
    SIGNED = 1
    UNSIGNED = 2
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return DnssecStatusId[obj]
        else:
            return DnssecStatusId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "SIGNED": "Signed",
            "UNSIGNED": "Unsigned",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Whois(Object):
    schema_name: ClassVar[str] = "whois"

    # Recommended
    created_time: datetime | None = None
    dnssec_status_id: DnssecStatusId | None = None
    domain: str | None = None
    domain_contacts: list[DomainContact] | None = None
    last_seen_time: datetime | None = None
    name_servers: list[str] | None = None
    registrar: str | None = None
    status: str | None = None

    # Optional
    autonomous_system: AutonomousSystem | None = None
    dnssec_status: str | None = None
    email_addr: EmailStr | None = None
    isp: str | None = None
    isp_org: str | None = None
    phone_number: str | None = None
    subdomains: list[str] | None = None
    subnet: IPvAnyNetwork | None = None
