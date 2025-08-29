from enum import Enum, property as enum_property
from typing import Any, ClassVar

from pydantic import IPvAnyAddress, model_validator
from pydantic_extra_types.mac_address import MacAddress

from ocsf.objects._entity import Entity
from ocsf.objects.port_info import PortInfo


class TypeId(Enum):
    UNKNOWN = 0
    WIRED = 1
    WIRELESS = 2
    MOBILE = 3
    TUNNEL = 4
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
            "WIRED": "Wired",
            "WIRELESS": "Wireless",
            "MOBILE": "Mobile",
            "TUNNEL": "Tunnel",
            "OTHER": "Other",
        }
        return name_map[super().name]


class NetworkInterface(Entity):
    schema_name: ClassVar[str] = "network_interface"

    # Recommended
    hostname: str | None = None
    ip: IPvAnyAddress | None = None
    mac: MacAddress | None = None
    name: str | None = None
    type_id: TypeId | None = None

    # Optional
    namespace: str | None = None
    open_ports: list[PortInfo] | None = None
    subnet_prefix: int | None = None
    type_: str | None = None
    uid: str | None = None

    @model_validator(mode="after")
    def validate_at_least_one(self):
        if all(getattr(self, field) is None for field in ["ip", "mac", "name", "hostname", "uid"]):
            raise ValueError("At least one of `ip`, `mac`, `name`, `hostname`, `uid` must be provided")
        return self
