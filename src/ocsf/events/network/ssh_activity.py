from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.events.network.network import Network
from ocsf.objects.file import File
from ocsf.objects.hassh import Hassh


class ActivityId(Enum):
    UNKNOWN = 0
    OPEN = 1
    CLOSE = 2
    RESET = 3
    FAIL = 4
    REFUSE = 5
    TRAFFIC = 6
    LISTEN = 7
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
            "OPEN": "Open",
            "CLOSE": "Close",
            "RESET": "Reset",
            "FAIL": "Fail",
            "REFUSE": "Refuse",
            "TRAFFIC": "Traffic",
            "LISTEN": "Listen",
            "OTHER": "Other",
        }
        return name_map[super().name]


class AuthTypeId(Enum):
    UNKNOWN = 0
    CERTIFICATE_BASED = 1
    GSSAPI = 2
    HOST_BASED = 3
    KEYBOARD_INTERACTIVE = 4
    PASSWORD = 5
    PUBLIC_KEY = 6
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return AuthTypeId[obj]
        else:
            return AuthTypeId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "CERTIFICATE_BASED": "Certificate Based",
            "GSSAPI": "GSSAPI",
            "HOST_BASED": "Host Based",
            "KEYBOARD_INTERACTIVE": "Keyboard Interactive",
            "PASSWORD": "Password",
            "PUBLIC_KEY": "Public Key",
            "OTHER": "Other",
        }
        return name_map[super().name]


class SshActivity(Network):
    schema_name: ClassVar[str] = "ssh_activity"
    class_id: int = 4007
    class_name: str = "SSH Activity"

    # Required
    activity_id: ActivityId

    # Recommended
    auth_type: str | None = None
    auth_type_id: AuthTypeId | None = None
    client_hassh: Hassh | None = None
    protocol_ver: str | None = None
    server_hassh: Hassh | None = None

    # Optional
    file: File | None = None
