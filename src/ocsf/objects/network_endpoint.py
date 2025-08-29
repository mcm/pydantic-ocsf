from enum import Enum, property as enum_property
from typing import Annotated, Any, ClassVar, TYPE_CHECKING

from annotated_types import Ge, Lt
from pydantic import IPvAnyAddress, model_validator

from ocsf.objects.autonomous_system import AutonomousSystem
from ocsf.objects.endpoint import Endpoint

if TYPE_CHECKING:
    from ocsf.objects.network_proxy import NetworkProxy


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


class NetworkEndpoint(Endpoint):
    schema_name: ClassVar[str] = "network_endpoint"

    # Recommended
    port: Annotated[int, Ge(0), Lt(65536)] | None = None
    svc_name: str | None = None
    type_id: TypeId | None = None

    # Optional
    autonomous_system: AutonomousSystem | None = None
    intermediate_ips: list[IPvAnyAddress] | None = None
    isp: str | None = None
    isp_org: str | None = None
    proxy_endpoint: "NetworkProxy | None" = None
    type_: str | None = None

    @model_validator(mode="after")
    def validate_at_least_one(self):
        if all(
            getattr(self, field) is None
            for field in [
                "ip",
                "uid",
                "name",
                "hostname",
                "svc_name",
                "instance_uid",
                "interface_uid",
                "interface_name",
                "domain",
            ]
        ):
            raise ValueError(
                "At least one of `ip`, `uid`, `name`, `hostname`, `svc_name`, `instance_uid`, `interface_uid`, `interface_name`, `domain` must be provided"
            )
        return self
