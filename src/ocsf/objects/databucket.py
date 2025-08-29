from datetime import datetime
from enum import Enum, property as enum_property
from typing import Any, ClassVar

from pydantic import IPvAnyAddress

from ocsf.objects._resource import Resource
from ocsf.objects.agent import Agent
from ocsf.objects.encryption_details import EncryptionDetails
from ocsf.objects.file import File
from ocsf.objects.graph import Graph
from ocsf.objects.group import Group
from ocsf.objects.user import User


class TypeId(Enum):
    UNKNOWN = 0
    S3 = 1
    AZURE_BLOB = 2
    GCP_BUCKET = 3
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
            "S3": "S3",
            "AZURE_BLOB": "Azure Blob",
            "GCP_BUCKET": "GCP Bucket",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Databucket(Resource):
    schema_name: ClassVar[str] = "databucket"

    # Required
    type_id: TypeId

    # Recommended
    hostname: str | None = None
    ip: IPvAnyAddress | None = None
    is_public: bool | None = None
    name: str | None = None
    owner: User | None = None
    type_: str | None = None
    uid: str | None = None

    # Optional
    agent_list: list[Agent] | None = None
    cloud_partition: str | None = None
    created_time: datetime | None = None
    criticality: str | None = None
    desc: str | None = None
    encryption_details: EncryptionDetails | None = None
    file: File | None = None
    group: Group | None = None
    groups: list[Group] | None = None
    is_backed_up: bool | None = None
    is_encrypted: bool | None = None
    modified_time: datetime | None = None
    namespace: str | None = None
    region: str | None = None
    resource_relationship: Graph | None = None
    size: int | None = None
    version: str | None = None
    zone: str | None = None
