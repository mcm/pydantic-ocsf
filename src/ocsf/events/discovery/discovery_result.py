from enum import Enum, property as enum_property
from typing import Annotated, Any, ClassVar, Literal

from pydantic import Field

from ocsf.events.base_event import BaseEvent
from ocsf.objects.query_info import QueryInfo


class ActivityId(Enum):
    UNKNOWN = 0
    QUERY = 1
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
            "QUERY": "Query",
            "OTHER": "Other",
        }
        return name_map[super().name]


class QueryResultId(Enum):
    UNKNOWN = 0
    EXISTS = 1
    PARTIAL = 2
    DOES_NOT_EXIST = 3
    ERROR = 4
    UNSUPPORTED = 5
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return QueryResultId[obj]
        else:
            return QueryResultId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "EXISTS": "Exists",
            "PARTIAL": "Partial",
            "DOES_NOT_EXIST": "Does not exist",
            "ERROR": "Error",
            "UNSUPPORTED": "Unsupported",
            "OTHER": "Other",
        }
        return name_map[super().name]


class DiscoveryResult(BaseEvent):
    schema_name: ClassVar[str] = "discovery_result"
    category_name: Annotated[Literal["Discovery"], Field(frozen=True)] = "Discovery"
    category_uid: Annotated[Literal[5], Field(frozen=True)] = 5

    # Required
    activity_id: ActivityId
    query_result_id: QueryResultId

    # Recommended
    query_info: QueryInfo | None = None
    query_result: str | None = None
