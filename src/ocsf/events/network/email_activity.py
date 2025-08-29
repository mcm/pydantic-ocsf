from enum import Enum, property as enum_property
from typing import Annotated, Any, ClassVar, Literal

from pydantic import EmailStr, Field

from ocsf.events.base_event import BaseEvent
from ocsf.objects.email import Email
from ocsf.objects.email_auth import EmailAuth
from ocsf.objects.network_endpoint import NetworkEndpoint


class ActivityId(Enum):
    UNKNOWN = 0
    SEND = 1
    RECEIVE = 2
    SCAN = 3
    TRACE = 4
    MTA_RELAY = 5
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
            "SEND": "Send",
            "RECEIVE": "Receive",
            "SCAN": "Scan",
            "TRACE": "Trace",
            "MTA_RELAY": "MTA Relay",
            "OTHER": "Other",
        }
        return name_map[super().name]


class DirectionId(Enum):
    UNKNOWN = 0
    INBOUND = 1
    OUTBOUND = 2
    INTERNAL = 3
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return DirectionId[obj]
        else:
            return DirectionId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "INBOUND": "Inbound",
            "OUTBOUND": "Outbound",
            "INTERNAL": "Internal",
            "OTHER": "Other",
        }
        return name_map[super().name]


class EmailActivity(BaseEvent):
    schema_name: ClassVar[str] = "email_activity"
    category_name: Annotated[Literal["Network Activity"], Field(frozen=True)] = "Network Activity"
    category_uid: Annotated[Literal[4], Field(frozen=True)] = 4

    # Required
    activity_id: ActivityId
    direction_id: DirectionId
    email: Email

    # Recommended
    command: str | None = None
    dst_endpoint: NetworkEndpoint | None = None
    email_auth: EmailAuth | None = None
    from_: EmailStr | None = None
    message_trace_uid: str | None = None
    protocol_name: str | None = None
    smtp_hello: str | None = None
    src_endpoint: NetworkEndpoint | None = None
    to: list[EmailStr] | None = None

    # Optional
    attempt: int | None = None
    banner: str | None = None
    direction: str | None = None
