from typing import Annotated, ClassVar, Literal

from pydantic import Field

from ocsf.events.base_event import BaseEvent


class Application(BaseEvent):
    schema_name: ClassVar[str] = "application"
    category_name: Annotated[Literal["Application Activity"], Field(frozen=True)] = "Application Activity"
    category_uid: Annotated[Literal[6], Field(frozen=True)] = 6
