from enum import Enum, property as enum_property
from typing import Annotated, Any, ClassVar, Literal

from pydantic import Field

from ocsf.events.base_event import BaseEvent
from ocsf.objects.url import Url


class ActivityId(Enum):
    UNKNOWN = 0
    SEND = 1
    RECEIVE = 2
    SCAN = 3
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
            "OTHER": "Other",
        }
        return name_map[super().name]


class EmailUrlActivity(BaseEvent):
    schema_name: ClassVar[str] = "email_url_activity"
    category_name: Annotated[Literal["Network Activity"], Field(frozen=True)] = "Network Activity"
    category_uid: Annotated[Literal[4], Field(frozen=True)] = 4

    # Required
    activity_id: ActivityId
    email_uid: str
    url: Url
