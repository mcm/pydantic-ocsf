from datetime import datetime
from enum import Enum, property as enum_property
from typing import Any, ClassVar
from uuid import UUID

from pydantic import IPvAnyAddress, IPvAnyNetwork

from ocsf.objects.endpoint import Endpoint
from ocsf.objects.group import Group
from ocsf.objects.image import Image
from ocsf.objects.location import Location
from ocsf.objects.network_interface import NetworkInterface
from ocsf.objects.organization import Organization


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
    SERVER = 1
    DESKTOP = 2
    LAPTOP = 3
    TABLET = 4
    MOBILE = 5
    VIRTUAL = 6
    IOT = 7
    BROWSER = 8
    FIREWALL = 9
    SWITCH = 10
    HUB = 11
    ROUTER = 12
    IDS = 13
    IPS = 14
    LOAD_BALANCER = 15
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
            "SERVER": "Server",
            "DESKTOP": "Desktop",
            "LAPTOP": "Laptop",
            "TABLET": "Tablet",
            "MOBILE": "Mobile",
            "VIRTUAL": "Virtual",
            "IOT": "IOT",
            "BROWSER": "Browser",
            "FIREWALL": "Firewall",
            "SWITCH": "Switch",
            "HUB": "Hub",
            "ROUTER": "Router",
            "IDS": "IDS",
            "IPS": "IPS",
            "LOAD_BALANCER": "Load Balancer",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Device(Endpoint):
    schema_name: ClassVar[str] = "device"

    # Required
    type_id: TypeId

    # Recommended
    hostname: str | None = None
    region: str | None = None
    type_: str | None = None
    uid: str | None = None
    vendor_name: str | None = None

    # Optional
    autoscale_uid: str | None = None
    boot_time: datetime | None = None
    boot_uid: str | None = None
    created_time: datetime | None = None
    desc: str | None = None
    domain: str | None = None
    eid: str | None = None
    first_seen_time: datetime | None = None
    groups: list[Group] | None = None
    hypervisor: str | None = None
    iccid: str | None = None
    image: Image | None = None
    imei: str | None = None
    imei_list: list[str] | None = None
    ip: IPvAnyAddress | None = None
    is_backed_up: bool | None = None
    is_compliant: bool | None = None
    is_managed: bool | None = None
    is_mobile_account_active: bool | None = None
    is_personal: bool | None = None
    is_shared: bool | None = None
    is_supervised: bool | None = None
    is_trusted: bool | None = None
    last_seen_time: datetime | None = None
    location: Location | None = None
    meid: str | None = None
    model: str | None = None
    modified_time: datetime | None = None
    name: str | None = None
    network_interfaces: list[NetworkInterface] | None = None
    org: Organization | None = None
    os_machine_uuid: UUID | None = None
    risk_level: str | None = None
    risk_level_id: RiskLevelId | None = None
    risk_score: int | None = None
    subnet: IPvAnyNetwork | None = None
    udid: str | None = None
    uid_alt: str | None = None
