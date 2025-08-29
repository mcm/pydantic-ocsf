from enum import Enum, property as enum_property
from typing import Any, ClassVar

from pydantic import IPvAnyAddress

from ocsf.objects._resource import Resource
from ocsf.objects.agent import Agent
from ocsf.objects.graph import Graph
from ocsf.objects.group import Group
from ocsf.objects.user import User


class RoleId(Enum):
    UNKNOWN = 0
    TARGET = 1
    ACTOR = 2
    AFFECTED = 3
    RELATED = 4
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return RoleId[obj]
        else:
            return RoleId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "TARGET": "Target",
            "ACTOR": "Actor",
            "AFFECTED": "Affected",
            "RELATED": "Related",
            "OTHER": "Other",
        }
        return name_map[super().name]


class ResourceDetails(Resource):
    schema_name: ClassVar[str] = "resource_details"

    # Recommended
    hostname: str | None = None
    ip: IPvAnyAddress | None = None
    name: str | None = None
    owner: User | None = None
    role_id: RoleId | None = None

    # Optional
    agent_list: list[Agent] | None = None
    cloud_partition: str | None = None
    criticality: str | None = None
    group: Group | None = None
    is_backed_up: bool | None = None
    namespace: str | None = None
    region: str | None = None
    resource_relationship: Graph | None = None
    role: str | None = None
    version: str | None = None
    zone: str | None = None
