from datetime import datetime
from enum import Enum, property as enum_property
from typing import Any, ClassVar

from pydantic import AnyUrl

from ocsf.objects._entity import Entity
from ocsf.objects.digital_signature import DigitalSignature
from ocsf.objects.encryption_details import EncryptionDetails
from ocsf.objects.fingerprint import Fingerprint
from ocsf.objects.key_value_object import KeyValueObject
from ocsf.objects.product import Product
from ocsf.objects.url import Url
from ocsf.objects.user import User


class ConfidentialityId(Enum):
    UNKNOWN = 0
    NOT_CONFIDENTIAL = 1
    CONFIDENTIAL = 2
    SECRET = 3
    TOP_SECRET = 4
    PRIVATE = 5
    RESTRICTED = 6
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return ConfidentialityId[obj]
        else:
            return ConfidentialityId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "NOT_CONFIDENTIAL": "Not Confidential",
            "CONFIDENTIAL": "Confidential",
            "SECRET": "Secret",
            "TOP_SECRET": "Top Secret",
            "PRIVATE": "Private",
            "RESTRICTED": "Restricted",
            "OTHER": "Other",
        }
        return name_map[super().name]


class DriveTypeId(Enum):
    UNKNOWN = 0
    REMOVABLE = 1
    FIXED = 2
    REMOTE = 3
    CD_ROM = 4
    RAM_DISK = 5
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return DriveTypeId[obj]
        else:
            return DriveTypeId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "REMOVABLE": "Removable",
            "FIXED": "Fixed",
            "REMOTE": "Remote",
            "CD_ROM": "CD-ROM",
            "RAM_DISK": "RAM Disk",
            "OTHER": "Other",
        }
        return name_map[super().name]


class TypeId(Enum):
    UNKNOWN = 0
    REGULAR_FILE = 1
    FOLDER = 2
    CHARACTER_DEVICE = 3
    BLOCK_DEVICE = 4
    LOCAL_SOCKET = 5
    NAMED_PIPE = 6
    SYMBOLIC_LINK = 7
    EXECUTABLE_FILE = 8
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
            "REGULAR_FILE": "Regular File",
            "FOLDER": "Folder",
            "CHARACTER_DEVICE": "Character Device",
            "BLOCK_DEVICE": "Block Device",
            "LOCAL_SOCKET": "Local Socket",
            "NAMED_PIPE": "Named Pipe",
            "SYMBOLIC_LINK": "Symbolic Link",
            "EXECUTABLE_FILE": "Executable File",
            "OTHER": "Other",
        }
        return name_map[super().name]


class File(Entity):
    schema_name: ClassVar[str] = "file"

    # Required
    name: str
    type_id: TypeId

    # Recommended
    ext: str | None = None
    hashes: list[Fingerprint] | None = None
    path: str | None = None

    # Optional
    accessed_time: datetime | None = None
    accessor: User | None = None
    attributes: int | None = None
    company_name: str | None = None
    confidentiality: str | None = None
    confidentiality_id: ConfidentialityId | None = None
    created_time: datetime | None = None
    creator: User | None = None
    desc: str | None = None
    drive_type: str | None = None
    drive_type_id: DriveTypeId | None = None
    encryption_details: EncryptionDetails | None = None
    internal_name: str | None = None
    is_deleted: bool | None = None
    is_encrypted: bool | None = None
    is_public: bool | None = None
    is_readonly: bool | None = None
    is_system: bool | None = None
    mime_type: str | None = None
    modified_time: datetime | None = None
    modifier: User | None = None
    owner: User | None = None
    parent_folder: str | None = None
    product: Product | None = None
    security_descriptor: str | None = None
    signature: DigitalSignature | None = None
    size: int | None = None
    storage_class: str | None = None
    tags: list[KeyValueObject] | None = None
    type_: str | None = None
    uid: str | None = None
    uri: AnyUrl | None = None
    url: Url | None = None
    version: str | None = None
    volume: str | None = None
    xattributes: dict[str, Any] | None = None
