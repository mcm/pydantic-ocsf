from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.events.network.network import Network
from ocsf.objects.dce_rpc import DceRpc
from ocsf.objects.file import File
from ocsf.objects.response import Response


class ActivityId(Enum):
    UNKNOWN = 0
    FILE_SUPERSEDE = 1
    FILE_OPEN = 2
    FILE_CREATE = 3
    FILE_OPEN_IF = 4
    FILE_OVERWRITE = 5
    FILE_OVERWRITE_IF = 6
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return ActivityId[obj]
        else:
            return ActivityId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "FILE_SUPERSEDE": "File Supersede",
            "FILE_OPEN": "File Open",
            "FILE_CREATE": "File Create",
            "FILE_OPEN_IF": "File Open If",
            "FILE_OVERWRITE": "File Overwrite",
            "FILE_OVERWRITE_IF": "File Overwrite If",
            "OTHER": "Other",
        }
        return name_map[super().name]


class ShareTypeId(Enum):
    UNKNOWN = 0
    FILE = 1
    PIPE = 2
    PRINT = 3
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return ShareTypeId[obj]
        else:
            return ShareTypeId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "FILE": "File",
            "PIPE": "Pipe",
            "PRINT": "Print",
            "OTHER": "Other",
        }
        return name_map[super().name]


class SmbActivity(Network):
    schema_name: ClassVar[str] = "smb_activity"
    class_id: int = 4006
    class_name: str = "SMB Activity"

    # Required
    activity_id: ActivityId

    # Recommended
    client_dialects: list[str] | None = None
    command: str | None = None
    dialect: str | None = None
    file: File | None = None
    open_type: str | None = None
    response: Response | None = None
    share: str | None = None
    share_type: str | None = None
    share_type_id: ShareTypeId | None = None
    tree_uid: str | None = None

    # Optional
    dce_rpc: DceRpc | None = None
